"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
DATE CREATED: 21/10/2023
DATE MODIFIED: 27/10/2023

Main Module to Run the System
"""

# Importing Functions from Different Modules
from Functions.main_menu import main_menu
from Functions.login import login
from Functions.clear_screen import clear_screen
from Functions.main_functions import load_books_from_csv

# Main Function
def main():
    username = login()

    user_roles = {
        'admin': 'admin',
        'customer': 'customer'
    }

    if username in user_roles:
        user_role = user_roles[username]

        while True:
            print(f"Logged in as: {username}")
            clear_screen()

            # Call the appropriate main menu function based on the user role
            main_menu(user_role)
    else:
        print("Invalid username")

if __name__ == "__main__":
    load_books_from_csv()
    main()
