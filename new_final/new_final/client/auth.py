from client.api import APIClient
from client.utils import validate_email

def signup_flow(api: APIClient):
    print("\n--- Sign Up ---")
    username = input("Username: ")
    email = input("Email: ")
    if not validate_email(email):
        print("Invalid email format.")
        return
    password = input("Password: ")
    resp = api.register(username, email, password)
    if resp.ok:
        print("Registration successful! Please log in.")
    else:
        print(f"Registration failed: {resp.json().get('detail', resp.text)}")

def login_flow(api: APIClient):
    print("\n--- Login ---")
    email = input("Email: ")
    password = input("Password: ")
    resp = api.login(email, password)
    if resp.ok:
        print("Login successful!")
        return True
    else:
        print(f"Login failed: {resp.json().get('detail', resp.text)}")
        return False 