"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
DATE CREATED: 21/10/2023
DATE MODIFIED: 24/10/2023

Module to validate user login
"""

# Function to perform user login with validation and login attempt limit
def login(max_attempts=3):
    print("---------- Library Management System - Login ----------")

    # Predefined username and password
    correct_username = "admin"
    correct_password = "password"

    customer_username = 'customer'
    customer_password = 'password'

    attempts = 0

    while attempts < max_attempts:
        # Input username and password
        username = input("Username: ")
        password = input("Password: ")

        if username == correct_username and password == correct_password:
            print("Login successful. Welcome, {}!".format(username))
            input("Press Enter to continue...")

            # Return the username upon successful login
            return username

        elif username == customer_username and password == customer_password:
            print("Login successful. Welcome, {}!".format(username))
            input("Press Enter to continue...")

            # Return the username upon successful login
            return username

        else:
            attempts += 1
            print(f"Login failed (Attempt {attempts}/{max_attempts}). Please check your credentials.")

    print("Maximum login attempts reached. Exiting.")
    input("Press Enter to continue...")

    return None
