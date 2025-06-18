import requests
import os
from typing import Optional, Dict, Any
import getpass
import re

class BaseClient:
    def __init__(self, base_url: str = "http://localhost:8000/api/v1"):
        self.base_url = base_url
        self.token = None
        self.user_info = None

    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title: str):
        """Print a formatted header"""
        print("=" * 60)
        print(f"{title:^60}")
        print("=" * 60)

    def print_menu(self, title: str, options: list):
        """Print a formatted menu"""
        self.print_header(title)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("=" * 60)

    def make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to the server"""
        url = f"{self.base_url}{endpoint}"
        
        if headers is None:
            headers = {}
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = response.json().get("detail", "Unknown error")
                return {"error": error_msg}
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to server. Please make sure the server is running."}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}

    def validate_email(self, email: str) -> bool:
        """Basic email validation"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def logout(self):
        """Logout user"""
        self.token = None
        self.user_info = None
        print("Logged out successfully!") 