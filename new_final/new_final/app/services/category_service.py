from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def create_category(self, category: CategoryCreate):
        if self.repo.get_by_name(category.category_name):
            raise ValueError("Category already exists")
        return self.repo.create(category)

    def get_category(self, category_id: int):
        return self.repo.get(category_id)

    def get_all_categories(self):
        return self.repo.get_all() 