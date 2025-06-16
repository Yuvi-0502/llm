from .base_view import BaseView

class AuthView(BaseView):
    def show_welcome(self):
        self.clear_screen()
        self.show_panel(
            "News Aggregation System",
            "Welcome to the News Aggregation Console Application"
        )

    def show_login_menu(self):
        self.clear_screen()
        self.show_panel("Login Menu", "1. Login\n2. Sign Up\n3. Exit")
        return self.get_input("Select an option", choices=["1", "2", "3"])

    def get_login_credentials(self):
        self.clear_screen()
        self.show_panel("Login", "Please enter your credentials")
        email = self.get_input("Email")
        password = self.get_input("Password", password=True)
        return email, password

    def get_signup_credentials(self):
        self.clear_screen()
        self.show_panel("Sign Up", "Please enter your details")
        username = self.get_input("Username")
        email = self.get_input("Email")
        password = self.get_input("Password", password=True)
        confirm_password = self.get_input("Confirm Password", password=True)
        return username, email, password, confirm_password 