import unittest

from models.book import Book
from models.library import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.book1 = Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
        self.book2 = Book("To Kill a Mockingbird", "Harper Lee", "9780060935467")

        self.library.add_book(self.book1)
        self.library.add_book(self.book2)

    def test_add_book_appends_book(self):
        book3 = Book("1984", "George Orwell", "9780451524935")

        self.library.add_book(book3)

        self.assertIn(book3, self.library.books)
        self.assertEqual(len(self.library.books), 3)

    def test_remove_book_removes_matching_isbn(self):
        self.library.remove_book("9780743273565")

        self.assertNotIn(self.book1, self.library.books)
        self.assertEqual(len(self.library.books), 1)

    def test_remove_book_leaves_books_when_isbn_missing(self):
        self.library.remove_book("0000000000")

        self.assertEqual(len(self.library.books), 2)

    def test_borrow_book_success(self):
        result = self.library.borrow_book("9780743273565")

        self.assertEqual(result, "You have borrowed 'The Great Gatsby'")
        self.assertFalse(self.book1.available)

    def test_borrow_book_fails_when_not_available(self):
        self.book1.available = False
        result = self.library.borrow_book("9780743273565")

        self.assertEqual(result, "Book not available")

    def test_borrow_book_fails_when_book_not_found(self):
        result = self.library.borrow_book("0000000000")

        self.assertEqual(result, "Book not available")

    def test_return_book_success(self):
        self.book1.available = False
        result = self.library.return_book("9780743273565")

        self.assertEqual(result, "You have returned 'The Great Gatsby'")
        self.assertTrue(self.book1.available)

    def test_return_book_fails_when_book_already_available(self):
        result = self.library.return_book("9780743273565")

        self.assertEqual(result, "Book not found or already available")

    def test_return_book_fails_when_book_not_found(self):
        result = self.library.return_book("0000000000")

        self.assertEqual(result, "Book not found or already available")
