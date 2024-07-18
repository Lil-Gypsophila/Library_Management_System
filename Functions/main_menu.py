"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
DATE CREATED: 21/10/2023
DATE MODIFIED: 27/10/2023

Main menu of the system
"""

import sys

from Functions.main_functions import add_book, display_books, search_book

def main_menu(user_role):
    while True:
        print("---------- Library Management System Main Menu ----------")
        print("1. List All Books")
        print("2. Search a Book")

        # Only admin able to add book
        if user_role == 'admin':
            print("3. Add a Book")

        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # List Books function
            print("Option 2: List Books")
            display_books(user_role)

        elif choice == "2":
            # Search a Book function
            print("Option 3: Search a Book")
            search_book()

        elif choice == "3":
            # Add a Book function
            print("Option 1: Add a Book")
            add_book()

        elif choice == "0":
            print("Exiting the system. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter a valid option.")
            input("Press Enter to continue...")
