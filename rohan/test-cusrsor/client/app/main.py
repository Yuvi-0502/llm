import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from datetime import datetime
from typing import Optional
import re
from app.api.client import APIClient

app = typer.Typer()
console = Console()
api_client = APIClient()


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def display_articles(articles: list, title: str = "Articles"):
    """Display articles in a table"""
    table = Table(title=title)
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Source", style="blue")
    table.add_column("Category", style="yellow")
    table.add_column("Published", style="magenta")

    for article in articles:
        table.add_row(
            str(article["id"]),
            article["title"],
            article["source"],
            article.get("category", {}).get("name", "N/A"),
            article["published_at"]
        )

    console.print(table)


@app.command()
def login():
    """Login to the application"""
    email = Prompt.ask("Email")
    password = Prompt.ask("Password", password=True)

    try:
        response = api_client.login(email, password)
        console.print("[green]Login successful![/green]")
        return response
    except Exception as e:
        console.print(f"[red]Login failed: {str(e)}[/red]")
        return None


@app.command()
def signup():
    """Sign up for a new account"""
    username = Prompt.ask("Username")
    email = Prompt.ask("Email")
    
    while not validate_email(email):
        console.print("[red]Invalid email format[/red]")
        email = Prompt.ask("Email")
    
    password = Prompt.ask("Password", password=True)
    confirm_password = Prompt.ask("Confirm Password", password=True)
    
    while password != confirm_password:
        console.print("[red]Passwords do not match[/red]")
        password = Prompt.ask("Password", password=True)
        confirm_password = Prompt.ask("Confirm Password", password=True)

    try:
        response = api_client.signup(username, email, password)
        console.print("[green]Signup successful! Please login.[/green]")
        return response
    except Exception as e:
        console.print(f"[red]Signup failed: {str(e)}[/red]")
        return None


@app.command()
def headlines(category: Optional[str] = None):
    """View news headlines"""
    try:
        articles = api_client.get_headlines(category)
        display_articles(articles, f"Headlines{f' - {category}' if category else ''}")
    except Exception as e:
        console.print(f"[red]Failed to fetch headlines: {str(e)}[/red]")


@app.command()
def saved():
    """View saved articles"""
    try:
        articles = api_client.get_saved_articles()
        display_articles(articles, "Saved Articles")
    except Exception as e:
        console.print(f"[red]Failed to fetch saved articles: {str(e)}[/red]")


@app.command()
def save(article_id: int):
    """Save an article"""
    try:
        response = api_client.save_article(article_id)
        console.print("[green]Article saved successfully![/green]")
        return response
    except Exception as e:
        console.print(f"[red]Failed to save article: {str(e)}[/red]")
        return None


@app.command()
def delete(article_id: int):
    """Delete a saved article"""
    try:
        response = api_client.delete_saved_article(article_id)
        console.print("[green]Article deleted successfully![/green]")
        return response
    except Exception as e:
        console.print(f"[red]Failed to delete article: {str(e)}[/red]")
        return None


@app.command()
def search(
    query: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Search articles"""
    try:
        articles = api_client.search_articles(query, start_date, end_date)
        display_articles(articles, f"Search Results for '{query}'")
    except Exception as e:
        console.print(f"[red]Failed to search articles: {str(e)}[/red]")


@app.command()
def notifications():
    """View notifications"""
    try:
        notifications = api_client.get_notifications()
        table = Table(title="Notifications")
        table.add_column("ID", style="cyan")
        table.add_column("Message", style="green")
        table.add_column("Created", style="blue")

        for notification in notifications:
            table.add_row(
                str(notification["id"]),
                notification["message"],
                notification["created_at"]
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Failed to fetch notifications: {str(e)}[/red]")


@app.command()
def configure_notifications():
    """Configure notification preferences"""
    try:
        preferences = {
            "Business": Confirm.ask("Enable Business notifications?"),
            "Technology": Confirm.ask("Enable Technology notifications?"),
            "Sports": Confirm.ask("Enable Sports notifications?"),
            "Entertainment": Confirm.ask("Enable Entertainment notifications?"),
        }
        
        response = api_client.update_notification_preferences(preferences)
        console.print("[green]Notification preferences updated successfully![/green]")
        return response
    except Exception as e:
        console.print(f"[red]Failed to update notification preferences: {str(e)}[/red]")
        return None


@app.command()
def add_keyword(keyword: str):
    """Add a keyword for notifications"""
    try:
        response = api_client.add_keyword(keyword)
        console.print("[green]Keyword added successfully![/green]")
        return response
    except Exception as e:
        console.print(f"[red]Failed to add keyword: {str(e)}[/red]")
        return None


@app.command()
def remove_keyword(keyword: str):
    """Remove a keyword"""
    try:
        response = api_client.remove_keyword(keyword)
        console.print("[green]Keyword removed successfully![/green]")
        return response
    except Exception as e:
        console.print(f"[red]Failed to remove keyword: {str(e)}[/red]")
        return None


# Admin commands
@app.command()
def list_servers():
    """List external servers (admin only)"""
    try:
        servers = api_client.get_external_servers()
        table = Table(title="External Servers")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="blue")
        table.add_column("Last Accessed", style="yellow")

        for server in servers:
            table.add_row(
                str(server["id"]),
                server["name"],
                "Active" if server["is_active"] else "Inactive",
                server["last_accessed"]
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Failed to fetch servers: {str(e)}[/red]")


@app.command()
def update_server(server_id: int, api_key: str):
    """Update external server details (admin only)"""
    try:
        response = api_client.update_external_server(server_id, api_key)
        console.print("[green]Server updated successfully![/green]")
        return response
    except Exception as e:
        console.print(f"[red]Failed to update server: {str(e)}[/red]")
        return None


@app.command()
def add_category(name: str, description: Optional[str] = None):
    """Add a new category (admin only)"""
    try:
        response = api_client.add_category(name, description)
        console.print("[green]Category added successfully![/green]")
        return response
    except Exception as e:
        console.print(f"[red]Failed to add category: {str(e)}[/red]")
        return None


if __name__ == "__main__":
    app() 