"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
DATE CREATED: 21/10/2023
DATE MODIFIED: 27/10/2023

Main functions of the system
"""

# Import Numpy for array
import numpy as np

from Functions.clear_screen import clear_screen
from Functions.validate_functions import *

# Path to the CSV file
book_csv_file = 'library_books.csv'

# Store in numpy array
books = np.array([])

# Define the number of books to display per page
BOOKS_PER_PAGE = 5

# Function to load books from the CSV file into the 'books' NumPy array
def load_books_from_csv():
    global books
    books = np.array([])  # Initialize the 'books' NumPy array

    if os.path.isfile(book_csv_file):
        with open(book_csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            books = np.array([row for row in reader])

# ADD A BOOK FUNCTION
def add_book():
    global books

    # Load the last assigned book ID
    next_id = get_last_assigned_book_id()

    clear_screen()
    print("Add a Book")

    # Adding Book Title
    title = validate_input("Title (or 'q' to quit): ", validate_title)
    if title is None:
        return  # Return to the main menu

    # Adding Book Author
    author = validate_input("Author (or 'q' to quit): ", validate_author)
    if author is None:
        return  # Return to the main menu

    # Adding Book ISBN
    isbn = validate_input("ISBN (5 digits, or 'q' to quit): ", validate_isbn)
    if isbn is None:
        return  # Return to the main menu

    # Generate a new book ID
    next_id += 1

    # Create a new book entry
    new_book = {"ID": next_id, "Title": title, "Author": author, "ISBN": isbn}

    # Append the new book to the existing books array
    books = np.append(books, new_book)

    # Save the book to the CSV file
    add_book_to_csv(new_book)

    input("Book added successfully. Press Enter to continue...")

# DISPLAY ALL BOOKS FUNCTION
def display_books(user_role):
    clear_screen()
    print("List of Books")

    try:
        # Check if the CSV file exists and contains data
        if not os.path.isfile(book_csv_file):
            print("No books available. The CSV file does not exist or is empty.")
            input("Press Enter to continue...")
            return

        with open(book_csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            books_from_csv = list(reader)

            if len(books_from_csv) == 0:
                print("No books available.")
                input("Press Enter to continue...")
                return

            # # Debugging: Print the contents of books_from_csv
            # print("Books from CSV:")
            # for book in books_from_csv:
            #     print(book)

            # Convert the books from CSV to a NumPy array to be display in table
            books_array = np.array(books_from_csv)

            # # Debugging: Print the contents of books
            # print("Books in NumPy array:")
            # for book in books_array:
            #     print(book)

        table = PrettyTable()
        table.field_names = ["ID", "Title", "Author", "ISBN"]

        for book in books_array:
            if "ID" in book:
                table.add_row([book["ID"], book.get("Title", ""), book.get("Author", ""), book.get("ISBN", "")])

        current_page = 1
        total_pages = (len(books_array) - 1) // BOOKS_PER_PAGE + 1

        while True:
            start_idx = (current_page - 1) * BOOKS_PER_PAGE
            end_idx = min(current_page * BOOKS_PER_PAGE, len(books_array))

            print(table.get_string(start = start_idx, end = end_idx))
            print(f"Page {current_page} / {total_pages}")

            user_input = input("1. Previous Page \n"
                               "2. Next Page \n" +
                               ("3. Update a book \n"
                                "4. Delete a book \n" if user_role == 'admin' else "") +
                               "0. Return to the main menu \n" +
                               "Enter your choice: ")

            if user_input == "1" and current_page > 1:
                current_page -= 1

                # Next Page
            elif user_input == "2" and current_page < total_pages:
                current_page += 1

            elif user_input == "3" and user_role == 'admin':
                update_book()
                break
            elif user_input == "4" and user_role == 'admin':
                delete_book()
                break
            elif user_input == "0":
                break
            else:
                print("Invalid choice. Returning to the main menu...")

        input("Returning to the main menu. Press Enter to continue...")

    except FileNotFoundError:
        print("The CSV file does not exists or is empty.")
        input("Press Enter to continue...")

# SEARCH FUNCTION BASED ON TITLE, AUTHOR AND ISBN
def search_book():
    global books

    clear_screen()
    print("Search for a Book")

    while True:
        query = input("Enter the title or author to search for: ")

        if query.lower() == 'q':

            # Quit to main menu
            return

        if not query:
            print("Please enter a search query.")
            input("Press Enter to continue.")

            # Restart the search function
            continue

        clear_screen()

        found_books = search_books(books, query)

        if found_books:
            print("Search Results:")
            display_search_results(found_books)
        else:
            print("No matching books found.")

        user_choice = input("1. Search for another book\n2. Return to the main menu\nEnter your choice: ")

        if user_choice == "2":

            # Return to the main menu
            return
        elif user_choice != "1":
            print("Invalid choice. Returning to the main menu...")
            return

# DELETE FUNCTION BASED ON ID
def delete_book():
    global books

    clear_screen()
    print("Delete a Book")

    while True:
        book_id = input("Enter the ID of the book to delete (or 'q' to quit): ")

        if book_id.lower() == 'q':
            return  # Quit the delete function

        # Convert the input to a string (book ID)
        try:
            book_id_str = str(book_id)
        except ValueError:
            print("Invalid input. Please enter a valid book ID.")
            continue

        # # Debugging code for book ID
        # print("Entered book_id:", book_id)
        # print("Book IDs in the dataset:", [str(book.get("ID", -1)) for book in books])

        # Search for the book based on the ID
        found_book_index = -1
        for i, book in enumerate(books):
            if "ID" in book and str(book["ID"]) == book_id_str:
                found_book_index = i
                break

        if found_book_index != -1:
            # Ask for confirmation before deletion
            confirmation = input("Are you sure you want to delete this book? (Y/n): ")

            if confirmation == 'Y':
                # Remove the book from the 'books' array
                books = np.delete(books, found_book_index)
                # Update the CSV file
                update_book_to_csv(books)
                print("Book deleted successfully.")
                input("Press Enter to continue.")
                return
            else:
                print("Deletion canceled.")
                input("Press Enter to continue.")
                return
        else:
            print("No book with the specified ID found.")

# UPDATE FUNCTION BASED ON ID
def update_book():
    global books

    clear_screen()
    print("Update Book Information")

    book_id = input("Enter the ID of the book you want to update: ")

    if book_id.lower() == 'q':
        return

    elif book_id.isdigit():
        book_id_str = str(book_id)
        found = False

        for index, book in enumerate(books):
            if str(book.get("ID")) == book_id_str:
                found = True

                # Display the current book information
                clear_screen()
                print("Current Book Information:")
                display_search_results([book])

                # Allow the user to update information
                # Update new Title
                new_title = input("New Title (or press Enter to keep the current title): ")

                # Return to the main menu
                if new_title.lower() == "q":
                    return

                # Update new Author
                new_author = input("New Author (or press Enter to keep the current author): ")
                if new_author.lower() == "q":
                    return  # Return to the main menu if the user enters 'q'

                elif new_author and not all(char.isalpha() or char.isspace() for char in new_author):
                    print("Invalid author format. Author should contain only alphabetic characters.")
                    return  # Return to the main menu if the input is invalid

                # Update new ISBN
                new_isbn = input("New ISBN (or press Enter to keep the current ISBN): ")
                if new_isbn.lower() == "q":
                    return  # Return to the main menu if the user enters 'q'

                elif new_isbn and not re.match(r'^\d{5}$', new_isbn):
                    print("Invalid ISBN format. ISBN should be a 5-digit number.")
                    return  # Return to the main menu if the input is invalid

                # Return to the main menu
                if new_isbn.lower() == "q":
                    return

                # Update the book information
                if new_title:
                    book["Title"] = new_title
                if new_author:
                    book["Author"] = new_author
                if new_isbn:
                    book["ISBN"] = new_isbn

                update_book_to_csv(books)

                if new_title or new_author or new_isbn:
                    print("Book information updated successfully.")
                else:
                    print("No information updated.")

                clear_screen()

        if not found:
            print("Book not found.")

    else:
        print("Invalid input. Please enter a valid book ID.")

    input("Press Enter to continue.")
