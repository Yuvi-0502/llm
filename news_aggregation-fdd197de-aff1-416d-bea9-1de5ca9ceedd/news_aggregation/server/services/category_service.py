from server.repos.category_repo import CategoryRepo


class CategoryService:
    def __init__(self):
        self.repo = CategoryRepo()

    def create_category(self, category_name):
        existing = self.repo.find_category(category_name)
        if existing:
            raise ValueError(f"Category '{category_name}' already exists")
        return self.repo.create_category(category_name)