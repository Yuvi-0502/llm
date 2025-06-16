from .base_view import BaseView
from ..models.external_server import ExternalServer

class AdminView(BaseView):
    def show_admin_menu(self):
        self.clear_screen()
        self.show_panel(
            "Admin Panel",
            "1. View External Servers\n"
            "2. Add External Server\n"
            "3. Edit External Server\n"
            "4. Delete External Server\n"
            "5. Back"
        )
        return self.get_input("Select an option", choices=["1", "2", "3", "4", "5"])

    def show_servers(self, servers: list[ExternalServer]):
        if not servers:
            self.show_warning("No servers found")
            return

        headers = ["Name", "Base URL", "Status"]
        rows = [
            [
                server.name,
                server.base_url,
                "Active" if server.is_active else "Inactive"
            ]
            for server in servers
        ]
        self.show_table("External Servers", headers, rows)

    def get_server_details(self, server: ExternalServer = None):
        self.clear_screen()
        title = "Edit Server" if server else "Add New Server"
        self.show_panel(title, "Enter server details")

        name = self.get_input("Server Name", default=server.name if server else "")
        api_key = self.get_input("API Key", default=server.api_key if server else "")
        base_url = self.get_input("Base URL", default=server.base_url if server else "")
        is_active = self.get_confirmation("Is server active?") if not server else self.get_confirmation(
            "Is server active?", default=server.is_active
        )

        return name, api_key, base_url, is_active

    def select_server(self, servers: list[ExternalServer]):
        self.clear_screen()
        self.show_panel("Select Server", "\n".join(
            f"{i+1}. {server.name} ({server.base_url})"
            for i, server in enumerate(servers)
        ))
        return self.get_input("Select a server", choices=[str(i) for i in range(1, len(servers) + 2)]) 