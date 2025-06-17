import re
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def pause():
    input("Press Enter to continue...") 