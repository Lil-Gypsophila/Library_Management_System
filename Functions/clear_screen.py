"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
DATE CREATED: 21/10/2023
DATE MODIFIED: 21/10/2023

Function clear the command line
"""

import os

# Function to clear the command line
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
