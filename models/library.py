from __future__ import annotations

from typing import List, TYPE_CHECKING

from models.book import Book

if TYPE_CHECKING:
    from models.database import Database


class Library:
    def __init__(self, connection_string: str | None = None):
        self._database: "Database" | None = None
        if connection_string:
            from models.database import Database

            self._database = Database(connection_string)
        self.books: List[Book] = self._database.load_books() if self._database else []

    def add_book(self, book: Book) -> None:
        if any(existing.isbn == book.isbn for existing in self.books):
            raise ValueError(f"A book with ISBN {book.isbn} already exists.")

        if self._database:
            self._database.add_book(book)
        self.books.append(book)

    def remove_book(self, isbn: str) -> None:
        if self._database:
            self._database.delete_book(isbn)
        self.books = [book for book in self.books if book.isbn != isbn]

    def borrow_book(self, isbn: str) -> str:
        if self._database:
            if self._database.borrow_book(isbn):
                for book in self.books:
                    if book.isbn == isbn:
                        book.available = False
                        return f"You have borrowed '{book.title}'"
                return f"You have borrowed '{isbn}'"
            return "Book not available"

        for book in self.books:
            if book.isbn == isbn and book.available:
                book.available = False
                return f"You have borrowed '{book.title}'"
        return "Book not available"

    def return_book(self, isbn: str) -> str:
        if self._database:
            if self._database.return_book(isbn):
                for book in self.books:
                    if book.isbn == isbn:
                        book.available = True
                        return f"You have returned '{book.title}'"
                return f"You have returned '{isbn}'"
            return "Book not found or already available"

        for book in self.books:
            if book.isbn == isbn and not book.available:
                book.available = True
                return f"You have returned '{book.title}'"
        return "Book not found or already available"
