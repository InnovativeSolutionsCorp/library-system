# Create a Library class that:
# stores books
# adds books
# removes books
# borrows books
# returns books
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, isbn):
        self.books = [book for book in self.books if book.isbn != isbn]

    def borrow_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and book.available:
                book.available = False
                return f"You have borrowed '{book.title}'"
        return "Book not available"

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn and not book.available:
                book.available = True
                return f"You have returned '{book.title}'"
        return "Book not found or already available"