from __future__ import annotations

import pyodbc
from typing import List

from models.book import Book

DEFAULT_CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=library-system;"
    "Trusted_Connection=yes;"
    "Encrypt=no;"
)


class Database:
    def __init__(self, connection_string: str | None = None):
        self.connection_string = connection_string or DEFAULT_CONNECTION_STRING
        self.connection = self._connect()
        self._initialize_schema()

    def _connect(self) -> pyodbc.Connection:
        try:
            connection = pyodbc.connect(self.connection_string)
            connection.autocommit = True
            return connection
        except pyodbc.Error as exc:
            raise RuntimeError(
                "Unable to connect to SQL Server using the configured connection string. "
                "Make sure the database server is running and the ODBC driver is installed. "
                f"Error: {exc}"
            ) from exc

    def _initialize_schema(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            IF OBJECT_ID(N'dbo.Books', N'U') IS NULL
            CREATE TABLE dbo.Books (
                BookId INT IDENTITY PRIMARY KEY,
                Title NVARCHAR(255) NOT NULL,
                Author NVARCHAR(255) NOT NULL,
                ISBN NVARCHAR(50) NOT NULL UNIQUE,
                Available BIT NOT NULL DEFAULT 1,
                CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
            );
            """
        )
        cursor.execute(
            """
            IF OBJECT_ID(N'dbo.BorrowHistory', N'U') IS NULL
            CREATE TABLE dbo.BorrowHistory (
                HistoryId INT IDENTITY PRIMARY KEY,
                BookId INT NOT NULL REFERENCES dbo.Books(BookId),
                EventType NVARCHAR(20) NOT NULL,
                EventDate DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
            );
            """
        )

    def load_books(self) -> List[Book]:
        cursor = self.connection.cursor()
        cursor.execute("EXEC usp_GetAllBooks;")
        books = []
        for _, title, author, isbn, available, *_ in cursor.fetchall():
            books.append(Book(title, author, isbn, bool(available)))
        return books

    def add_book(self, book: Book) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "EXEC usp_AddBook ?, ?, ?;",
                book.title,
                book.author,
                book.isbn,
            )
        except pyodbc.Error as exc:
            message = str(exc).lower()
            if "duplicate" in message or "unique" in message:
                raise ValueError(f"A book with ISBN {book.isbn} already exists.") from exc
            raise

    def delete_book(self, isbn: str) -> None:
        cursor = self.connection.cursor()
        cursor.execute("EXEC usp_RemoveBook ?;", isbn)

    def borrow_book(self, isbn: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("EXEC usp_BorrowBook ?;", isbn)
        return cursor.rowcount > 0

    def return_book(self, isbn: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("EXEC usp_ReturnBook ?;", isbn)
        return cursor.rowcount > 0

    def _book_exists(self, isbn: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT 1 FROM dbo.Books WHERE ISBN = ?;", isbn)
        return cursor.fetchone() is not None
