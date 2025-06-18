from fastapi import HTTPException
from services.category_service import CategoryService
from schemas.category import CategoryCreate, CategoryUpdate
from Exceptions.exceptions import CategoryNotFoundException
from config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_NOT_FOUND
from typing import List

class CategoryController:
    def __init__(self):
        self.service = CategoryService()

    def get_all_categories(self) -> List[dict]:
        """Get all categories"""
        try:
            return self.service.get_all_categories()
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_category_by_id(self, category_id: int) -> dict:
        """Get category by ID"""
        try:
            return self.service.get_category_by_id(category_id)
        except CategoryNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def create_category(self, category: CategoryCreate) -> dict:
        """Create a new category"""
        try:
            return self.service.create_category(category.name, category.description)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def update_category(self, category_id: int, category: CategoryUpdate) -> dict:
        """Update a category"""
        try:
            return self.service.update_category(category_id, category.name, category.description)
        except CategoryNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete_category(self, category_id: int):
        """Delete a category"""
        try:
            self.service.delete_category(category_id)
            return {"message": f"Category {category_id} deleted successfully"}
        except CategoryNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e)) 