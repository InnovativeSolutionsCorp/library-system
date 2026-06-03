from models.book import Book; from models.library import Library
DEFAULT_CONNECTION_STRING = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=library-system;Trusted_Connection=yes;Encrypt=no;"; MENU = "\n=== Library Menu ===\n1. View all books\n2. Add a book\n3. Remove a book\n4. Borrow a book\n5. Return a book\n6. Search by title\n7. Search by author\n8. Exit"
def main() -> None:
    try: library = Library(DEFAULT_CONNECTION_STRING)
    except Exception as exc: print("Unable to connect to the library database:", exc); return
    if not library.books:
        for t,a,i in [("The Great Gatsby","F. Scott Fitzgerald","9780743273565"),("To Kill a Mockingbird","Harper Lee","9780060935467"),("1984","George Orwell","9780451524935")]:
            try: library.add_book(Book(t,a,i))
            except ValueError: pass
    while True:
        print(MENU)
        choice = input("Choose an option (1-8): ").strip()
        if choice == "1":
            if not library.books: print("No books are currently available in the library."); continue
            print("\nBooks in the library:"); [print(f"- {book}") for book in library.books]
        elif choice == "2":
            title = input("Title: ").strip(); author = input("Author: ").strip(); isbn = input("ISBN: ").strip()
            if not title or not author or not isbn: print("All fields are required. Please try again."); continue
            if any(book.isbn == isbn for book in library.books): print("A book with that ISBN already exists."); continue
            library.add_book(Book(title,author,isbn)); print(f"Added '{title}' by {author}.")
        elif choice == "3":
            isbn = input("Enter ISBN: ").strip()
            if not isbn: print("ISBN is required."); continue
            if not any(book.isbn == isbn for book in library.books): print("No book found with that ISBN."); continue
            library.remove_book(isbn); print(f"Removed book with ISBN {isbn}.")
        elif choice in ("4","5"):
            isbn = input("Enter ISBN: ").strip()
            if not isbn: print("ISBN is required."); continue
            print(library.borrow_book(isbn) if choice == "4" else library.return_book(isbn))
        elif choice in ("6","7"):
            field = "title" if choice == "6" else "author"
            query = input(f"Enter {field} search term: ").strip()
            if not query: print("Search term is required."); continue
            results = [book for book in library.books if query.lower() in getattr(book,field).lower()]
            if not results: print(f"No books found matching {field} '{query}'."); continue
            print(f"\nSearch results for {field} '{query}':"); [print(f"- {book}") for book in results]
        elif choice == "8": print("Goodbye!"); break
        else: print("Invalid choice. Please enter a number between 1 and 8.")
if __name__ == "__main__":
    main()