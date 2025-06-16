import os
import sys
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from services.api_client import APIClient

console = Console()

class NewsAggregationClient:
    def __init__(self):
        self.api_client = APIClient()
        self.current_user = None
        self.token = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_welcome(self):
        self.clear_screen()
        console.print(Panel.fit(
            "[bold blue]News Aggregation System[/bold blue]\n"
            "Welcome to the News Aggregation Console Application",
            border_style="blue"
        ))

    def login(self):
        while True:
            self.clear_screen()
            console.print("[bold]Login[/bold]")
            email = Prompt.ask("Email")
            password = Prompt.ask("Password", password=True)

            try:
                response = self.api_client.login(email, password)
                self.token = response["access_token"]
                self.current_user = response["user"]
                self.api_client.set_token(self.token)
                console.print("[green]Login successful![/green]")
                return True
            except Exception as e:
                console.print("[red]Invalid email or password[/red]")
                if not Confirm.ask("Try again?"):
                    return False

    def signup(self):
        while True:
            self.clear_screen()
            console.print("[bold]Sign Up[/bold]")
            username = Prompt.ask("Username")
            email = Prompt.ask("Email")
            password = Prompt.ask("Password", password=True)
            confirm_password = Prompt.ask("Confirm Password", password=True)

            if password != confirm_password:
                console.print("[red]Passwords do not match[/red]")
                if not Confirm.ask("Try again?"):
                    return False
                continue

            try:
                self.api_client.signup(username, email, password)
                console.print("[green]Account created successfully! Please login.[/green]")
                return True
            except Exception as e:
                console.print("[red]Error creating account[/red]")
                if not Confirm.ask("Try again?"):
                    return False

    def display_articles(self, articles):
        if not articles:
            console.print("[yellow]No articles found[/yellow]")
            return

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Title")
        table.add_column("Source")
        table.add_column("Category")
        table.add_column("Published")

        for article in articles:
            table.add_row(
                article["title"],
                article["source"],
                article["category"],
                article["published_at"]
            )

        console.print(table)

    def show_news_menu(self):
        while True:
            self.clear_screen()
            console.print("[bold]News Menu[/bold]")
            console.print("1. View All News")
            console.print("2. View by Category")
            console.print("3. Search News")
            console.print("4. View Saved Articles")
            if self.current_user.get("is_admin"):
                console.print("5. Admin Panel")
            console.print("6. Logout")
            console.print("7. Exit")

            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "7"])

            if choice == "1":
                self.view_all_news()
            elif choice == "2":
                self.view_by_category()
            elif choice == "3":
                self.search_news()
            elif choice == "4":
                self.view_saved_articles()
            elif choice == "5" and self.current_user.get("is_admin"):
                self.show_admin_panel()
            elif choice == "6":
                self.logout()
                return
            elif choice == "7":
                sys.exit(0)

    def view_all_news(self):
        self.clear_screen()
        console.print("[bold]All News[/bold]")
        try:
            articles = self.api_client.get_news()
            self.display_articles(articles)
        except Exception as e:
            console.print("[red]Error loading news[/red]")
        Prompt.ask("\nPress Enter to continue")

    def view_by_category(self):
        self.clear_screen()
        console.print("[bold]Categories[/bold]")
        categories = [
            "Business",
            "Technology",
            "Sports",
            "Entertainment",
            "Health",
            "Science"
        ]
        for i, category in enumerate(categories, 1):
            console.print(f"{i}. {category}")
        console.print(f"{len(categories) + 1}. Back")

        choice = Prompt.ask("Select a category", choices=[str(i) for i in range(1, len(categories) + 2)])
        if choice == str(len(categories) + 1):
            return

        try:
            articles = self.api_client.get_news(categories[int(choice) - 1])
            self.display_articles(articles)
        except Exception as e:
            console.print("[red]Error loading news[/red]")
        Prompt.ask("\nPress Enter to continue")

    def search_news(self):
        self.clear_screen()
        console.print("[bold]Search News[/bold]")
        query = Prompt.ask("Enter search query")
        try:
            articles = self.api_client.search_news(query)
            self.display_articles(articles)
        except Exception as e:
            console.print("[red]Error searching news[/red]")
        Prompt.ask("\nPress Enter to continue")

    def view_saved_articles(self):
        self.clear_screen()
        console.print("[bold]Saved Articles[/bold]")
        try:
            articles = self.api_client.get_saved_articles()
            self.display_articles(articles)
        except Exception as e:
            console.print("[red]Error loading saved articles[/red]")
        Prompt.ask("\nPress Enter to continue")

    def show_admin_panel(self):
        while True:
            self.clear_screen()
            console.print("[bold]Admin Panel[/bold]")
            console.print("1. View External Servers")
            console.print("2. Add External Server")
            console.print("3. Edit External Server")
            console.print("4. Delete External Server")
            console.print("5. Back")

            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])

            if choice == "1":
                self.view_external_servers()
            elif choice == "2":
                self.add_external_server()
            elif choice == "3":
                self.edit_external_server()
            elif choice == "4":
                self.delete_external_server()
            elif choice == "5":
                return

    def view_external_servers(self):
        self.clear_screen()
        console.print("[bold]External Servers[/bold]")
        try:
            servers = self.api_client.get_external_servers()
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("Name")
            table.add_column("Base URL")
            table.add_column("Status")

            for server in servers:
                table.add_row(
                    server["name"],
                    server["base_url"],
                    "[green]Active[/green]" if server["is_active"] else "[red]Inactive[/red]"
                )

            console.print(table)
        except Exception as e:
            console.print("[red]Error loading servers[/red]")
        Prompt.ask("\nPress Enter to continue")

    def add_external_server(self):
        self.clear_screen()
        console.print("[bold]Add External Server[/bold]")
        try:
            name = Prompt.ask("Server Name")
            api_key = Prompt.ask("API Key")
            base_url = Prompt.ask("Base URL")
            is_active = Confirm.ask("Is server active?")

            self.api_client.create_external_server({
                "name": name,
                "api_key": api_key,
                "base_url": base_url,
                "is_active": is_active
            })
            console.print("[green]Server added successfully![/green]")
        except Exception as e:
            console.print("[red]Error adding server[/red]")
        Prompt.ask("\nPress Enter to continue")

    def edit_external_server(self):
        self.clear_screen()
        console.print("[bold]Edit External Server[/bold]")
        try:
            servers = self.api_client.get_external_servers()
            for i, server in enumerate(servers, 1):
                console.print(f"{i}. {server['name']} ({server['base_url']})")
            console.print(f"{len(servers) + 1}. Back")

            choice = Prompt.ask("Select a server", choices=[str(i) for i in range(1, len(servers) + 2)])
            if choice == str(len(servers) + 1):
                return

            server = servers[int(choice) - 1]
            name = Prompt.ask("Server Name", default=server["name"])
            api_key = Prompt.ask("API Key", default=server["api_key"])
            base_url = Prompt.ask("Base URL", default=server["base_url"])
            is_active = Confirm.ask("Is server active?", default=server["is_active"])

            self.api_client.update_external_server(server["id"], {
                "name": name,
                "api_key": api_key,
                "base_url": base_url,
                "is_active": is_active
            })
            console.print("[green]Server updated successfully![/green]")
        except Exception as e:
            console.print("[red]Error updating server[/red]")
        Prompt.ask("\nPress Enter to continue")

    def delete_external_server(self):
        self.clear_screen()
        console.print("[bold]Delete External Server[/bold]")
        try:
            servers = self.api_client.get_external_servers()
            for i, server in enumerate(servers, 1):
                console.print(f"{i}. {server['name']} ({server['base_url']})")
            console.print(f"{len(servers) + 1}. Back")

            choice = Prompt.ask("Select a server", choices=[str(i) for i in range(1, len(servers) + 2)])
            if choice == str(len(servers) + 1):
                return

            if Confirm.ask("Are you sure you want to delete this server?"):
                server = servers[int(choice) - 1]
                self.api_client.delete_external_server(server["id"])
                console.print("[green]Server deleted successfully![/green]")
        except Exception as e:
            console.print("[red]Error deleting server[/red]")
        Prompt.ask("\nPress Enter to continue")

    def logout(self):
        self.current_user = None
        self.token = None
        self.api_client.set_token(None)
        console.print("[yellow]Logged out successfully[/yellow]")

    def run(self):
        while True:
            self.show_welcome()
            console.print("1. Login")
            console.print("2. Sign Up")
            console.print("3. Exit")

            choice = Prompt.ask("Select an option", choices=["1", "2", "3"])

            if choice == "1":
                if self.login():
                    self.show_news_menu()
            elif choice == "2":
                if self.signup():
                    if self.login():
                        self.show_news_menu()
            elif choice == "3":
                sys.exit(0)

if __name__ == "__main__":
    client = NewsAggregationClient()
    client.run() 