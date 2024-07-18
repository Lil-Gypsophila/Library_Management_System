"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
DATE CREATED: 21/10/2023
DATE MODIFIED: 27/10/2023

Supporting functions of the system
"""

# Import CSV file
import csv

# Import Operating System
import os

# Import Regex for validation
import re

# Import PrettyTable to display books in table format
from prettytable import PrettyTable

# Path to the CSV file
book_csv_file = 'library_books.csv'

# Function to check weather CSV file exists
def check_csv():
    # Check if the CSV file exists, and if not, create it
    if not os.path.isfile(book_csv_file):
        with open(book_csv_file, mode='w', newline='') as csvfile:
            fieldnames = ['ID', 'Title', 'Author', 'ISBN']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    # Check if the CSV file contains the header for 'Title' and add it if missing
    with open(book_csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        if 'Title' not in reader.fieldnames:
            add_title_header()

def add_title_header():
    # Read the existing content of the CSV file
    rows = []

    with open(book_csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]

    # Add the Title header to the CSV file
    if not rows:
        with open(book_csv_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['ID', 'Title', 'Author', 'ISBN'])
            writer.writeheader()

# Function to save a book to the CSV file
def add_book_to_csv(book):

    # Check the CSV file weather the header is there
    check_csv()

    # Add new book into the CSV file
    with open(book_csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([book["ID"], book["Title"], book["Author"], book["ISBN"]])

# Function to handle user input 'q' to return to the main menu
def validate_input(prompt, validation_func):
    while True:
        user_input = input(prompt)

        if user_input.lower() == 'q':
            input("Returning to the main menu. Press Enter to continue...")
            return None
        validation_result, error_message = validation_func(user_input)

        if validation_result is not None:
            return validation_result
        else:
            print(error_message)

# Function to validate title input
def validate_title(title):
    if not title.strip():  # Check if title is empty or contains only whitespace
        error_message = "Title is required and cannot be empty."
        return None, error_message

    return title, None

# Function to validate author input
def validate_author(author):
    if not author and not all(char.isalpha() or char.isspace() for char in author):
        error_message = "Invalid author format. Author should contain only alphabetic characters."
        return None, error_message

    return author, None

# Function to validate ISBN input
def validate_isbn(isbn):
    while not re.match(r'^\d{5}$', isbn):
        error_message = "Invalid ISBN format. ISBN should be a 5-digit number."
        return None, error_message

    return isbn, None

# Function to retrieve the last Book ID from the CSV file
def get_last_assigned_book_id():
    last_assigned_id = 0  # Initialize to 0 as a default

    try:
        with open(book_csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                book_id = int(row['ID'])
                if book_id > last_assigned_id:
                    last_assigned_id = book_id

    except FileNotFoundError:
        # Handle the case where the CSV file doesn't exist
        pass

    return last_assigned_id

# Function to save the entire books array to the CSV file
def update_book_to_csv(books):
    with open(book_csv_file, mode='w', newline='') as file:
        fieldnames = ['ID', 'Title', 'Author', 'ISBN']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header to the CSV file if it doesn't exist
        if not os.path.isfile(book_csv_file) or os.path.getsize(book_csv_file) == 0:
            writer.writeheader()

        for book in books:
            writer.writerow(book)

# SEARCH QUERY
def search_books(books, query):
    query = query.lower()
    found_books = []

    for book in books:
        title = book.get("Title", "").lower()
        author = book.get("Author", "").lower()
        isbn = book.get('ISBN', "")

        if query in title or query in author or query in isbn:
            found_books.append(book)

    return found_books

# Function to display search results
def display_search_results(books):
    if len(books) == 0:
        print("No books available.")
    else:
        table = PrettyTable()
        table.field_names = ["ID", "Title", "Author", "ISBN"]

        for book in books:
            table.add_row([book["ID"], book.get("Title", ""), book.get("Author", ""), book.get("ISBN", "")])

        print(table)
