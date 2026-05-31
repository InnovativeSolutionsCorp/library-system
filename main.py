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
    print("6. Search by title")
    print("7. Search by author")
    print("8. Exit")


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


def search_books(library: Library, query: str, field: str) -> list[Book]:
    query_lower = query.lower()
    if field == "title":
        return [book for book in library.books if query_lower in book.title.lower()]
    return [book for book in library.books if query_lower in book.author.lower()]


def print_search_results(results: list[Book], field: str, query: str) -> None:
    if not results:
        print(f"No books found matching {field} '{query}'.")
        return

    print(f"\nSearch results for {field} '{query}':")
    for book in results:
        print(f"- {book}")


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
            query = input("Enter title search term: ").strip()
            if not query:
                print("Search term is required.")
                continue
            results = search_books(library, query, "title")
            print_search_results(results, "title", query)
        elif choice == "7":
            query = input("Enter author search term: ").strip()
            if not query:
                print("Search term is required.")
                continue
            results = search_books(library, query, "author")
            print_search_results(results, "author", query)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    main()
