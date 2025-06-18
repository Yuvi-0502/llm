from Repositories.external_server_repo import ExternalServerRepository
from schemas.external_server import ExternalServerCreate, ExternalServerUpdate
from Exceptions.exceptions import ExternalServerNotFoundException
from typing import List

class ExternalServerService:
    def __init__(self):
        self.repo = ExternalServerRepository()

    def get_all_servers(self) -> List[dict]:
        return self.repo.get_all()

    def get_server_by_id(self, server_id: int) -> dict:
        server = self.repo.get_by_id(server_id)
        if not server:
            raise ExternalServerNotFoundException(f"Server with ID {server_id} not found")
        return server

    def create_server(self, server: ExternalServerCreate) -> dict:
        return self.repo.create(server)

    def update_server(self, server_id: int, server: ExternalServerUpdate) -> dict:
        existing_server = self.repo.get_by_id(server_id)
        if not existing_server:
            raise ExternalServerNotFoundException(f"Server with ID {server_id} not found")
        return self.repo.update(server_id, server)

    def delete_server(self, server_id: int):
        existing_server = self.repo.get_by_id(server_id)
        if not existing_server:
            raise ExternalServerNotFoundException(f"Server with ID {server_id} not found")
        self.repo.delete(server_id)

    def get_active_servers(self) -> List[dict]:
        return self.repo.get_active_servers()

    def update_last_accessed(self, server_id: int):
        self.repo.update_last_accessed(server_id)
