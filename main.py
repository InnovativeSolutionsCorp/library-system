from models.book import Book
from models.library import Library


def print_menu() -> None:
    print()
    print("=== Library Menu ===")
    print("1. View all books")
    print("2. Add a book")
    print("3. Remove a book")
    print("4. Borrow a book")
    print("5. Return a book")
    print("6. Exit")


def display_books(library: Library) -> None:
    if not library.books:
        print("No books are currently available in the library.")
        return

    print("\nBooks in the library:")
    for book in library.books:
        print(f"- {book}")


def prompt_book_details() -> tuple[str, str, str]:
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    isbn = input("ISBN: ").strip()
    return title, author, isbn


def prompt_isbn() -> str:
    return input("Enter ISBN: ").strip()


def main() -> None:
    library = Library()
    library.add_book(Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565"))
    library.add_book(Book("To Kill a Mockingbird", "Harper Lee", "9780060935467"))
    library.add_book(Book("1984", "George Orwell", "9780451524935"))

    while True:
        print_menu()
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            display_books(library)
        elif choice == "2":
            title, author, isbn = prompt_book_details()
            if not title or not author or not isbn:
                print("All fields are required. Please try again.")
                continue
            if any(book.isbn == isbn for book in library.books):
                print("A book with that ISBN already exists.")
                continue
            library.add_book(Book(title, author, isbn))
            print(f"Added '{title}' by {author}.")
        elif choice == "3":
            isbn = prompt_isbn()
            if not isbn:
                print("ISBN is required.")
                continue
            existing = [book for book in library.books if book.isbn == isbn]
            if not existing:
                print("No book found with that ISBN.")
                continue
            library.remove_book(isbn)
            print(f"Removed book with ISBN {isbn}.")
        elif choice == "4":
            isbn = prompt_isbn()
            if not isbn:
                print("ISBN is required.")
                continue
            print(library.borrow_book(isbn))
        elif choice == "5":
            isbn = prompt_isbn()
            if not isbn:
                print("ISBN is required.")
                continue
            print(library.return_book(isbn))
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
