# from fastapi import HTTPException
from server.services.category_service import CategoryService
from server.schemas.category import CategoryCreate
# from Exceptions.exceptions import CategoryNotFoundException
# from config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_NOT_FOUND
# from typing import List

class CategoryController:
    def __init__(self):
        self.service = CategoryService()

    def create_category(self, category: CategoryCreate):
        return self.service.create_category(category.name)