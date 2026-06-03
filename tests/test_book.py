import unittest

from models.book import Book


class TestBook(unittest.TestCase):
    def test_str_returns_title_author_isbn_available(self):
        book = Book("1984", "George Orwell", "9780451524935", available=True)

        self.assertEqual(
            str(book),
            "1984 by George Orwell (ISBN: 9780451524935) - Available",
        )

    def test_str_returns_not_available_when_borrowed(self):
        book = Book("1984", "George Orwell", "9780451524935", available=False)

        self.assertEqual(
            str(book),
            "1984 by George Orwell (ISBN: 9780451524935) - Not Available",
        )
