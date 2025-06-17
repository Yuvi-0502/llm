from app.repositories.external_server_repository import ExternalServerRepository
from app.repositories.category_repository import CategoryRepository
from app.schemas.external_server import ExternalServerCreate
from app.schemas.category import CategoryCreate

class AdminService:
    def __init__(self):
        self.server_repo = ExternalServerRepository()
        self.category_repo = CategoryRepository()

    def add_external_server(self, server: ExternalServerCreate):
        if self.server_repo.get_by_name(server.server_name):
            raise ValueError("Server already exists")
        return self.server_repo.create(server)

    def update_server_api_key(self, server_id: int, api_key: str):
        return self.server_repo.update_api_key(server_id, api_key)

    def get_all_servers(self):
        return self.server_repo.get_all()

    def get_server(self, server_id: int):
        return self.server_repo.get(server_id)

    def add_category(self, category: CategoryCreate):
        if self.category_repo.get_by_name(category.category_name):
            raise ValueError("Category already exists")
        return self.category_repo.create(category) 