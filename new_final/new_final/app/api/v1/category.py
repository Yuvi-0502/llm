from fastapi import APIRouter, HTTPException
from app.schemas.category import CategoryCreate, CategoryOut
from app.services.category_service import CategoryService
from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate):
    service = CategoryService()
    try:
        return service.create_category(category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int):
    service = CategoryService()
    category = service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/", response_model=List[CategoryOut])
def list_categories():
    service = CategoryService()
    return service.get_all_categories() 