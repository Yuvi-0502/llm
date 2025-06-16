import os
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel

class BaseView:
    def __init__(self):
        self.console = Console()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_error(self, message: str):
        self.console.print(f"[red]{message}[/red]")

    def show_success(self, message: str):
        self.console.print(f"[green]{message}[/green]")

    def show_warning(self, message: str):
        self.console.print(f"[yellow]{message}[/yellow]")

    def show_info(self, message: str):
        self.console.print(f"[blue]{message}[/blue]")

    def show_panel(self, title: str, content: str):
        self.console.print(Panel.fit(content, title=title, border_style="blue"))

    def show_table(self, title: str, headers: list, rows: list):
        table = Table(show_header=True, header_style="bold blue", title=title)
        for header in headers:
            table.add_column(header)
        for row in rows:
            table.add_row(*[str(cell) for cell in row])
        self.console.print(table)

    def get_input(self, prompt: str, password: bool = False) -> str:
        return Prompt.ask(prompt, password=password)

    def get_confirmation(self, prompt: str) -> bool:
        return Confirm.ask(prompt)

    def wait_for_enter(self):
        self.get_input("\nPress Enter to continue") 