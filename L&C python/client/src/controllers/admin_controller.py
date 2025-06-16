from typing import List
from ..models.external_server import ExternalServer
from ..services.api_client import APIClient

class AdminController:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get_external_servers(self) -> List[ExternalServer]:
        try:
            response = self.api_client.get_external_servers()
            return [ExternalServer(**server) for server in response]
        except Exception as e:
            raise Exception("Error loading external servers")

    def create_external_server(self, name: str, api_key: str, base_url: str, is_active: bool) -> ExternalServer:
        try:
            response = self.api_client.create_external_server({
                "name": name,
                "api_key": api_key,
                "base_url": base_url,
                "is_active": is_active
            })
            return ExternalServer(**response)
        except Exception as e:
            raise Exception("Error creating external server")

    def update_external_server(self, server_id: int, name: str, api_key: str, base_url: str, is_active: bool) -> ExternalServer:
        try:
            response = self.api_client.update_external_server(server_id, {
                "name": name,
                "api_key": api_key,
                "base_url": base_url,
                "is_active": is_active
            })
            return ExternalServer(**response)
        except Exception as e:
            raise Exception("Error updating external server")

    def delete_external_server(self, server_id: int) -> bool:
        try:
            self.api_client.delete_external_server(server_id)
            return True
        except Exception as e:
            raise Exception("Error deleting external server") 