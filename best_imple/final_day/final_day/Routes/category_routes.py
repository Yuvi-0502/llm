from fastapi import APIRouter, HTTPException, Depends
from schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from controllers.category_controller import CategoryController
from Utils.jwt_handler import admin_required
from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryResponse])
def get_all_categories(current_user=Depends(admin_required)):
    """Get all categories (Admin only)"""
    try:
        controller = CategoryController()
        return controller.get_all_categories()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_by_id(category_id: int, current_user=Depends(admin_required)):
    """Get category by ID (Admin only)"""
    try:
        controller = CategoryController()
        return controller.get_category_by_id(category_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=CategoryResponse)
def create_category(category: CategoryCreate, current_user=Depends(admin_required)):
    """Create new category (Admin only)"""
    try:
        controller = CategoryController()
        return controller.create_category(category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryUpdate, current_user=Depends(admin_required)):
    """Update category (Admin only)"""
    try:
        controller = CategoryController()
        return controller.update_category(category_id, category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{category_id}")
def delete_category(category_id: int, current_user=Depends(admin_required)):
    """Delete category (Admin only)"""
    try:
        controller = CategoryController()
        return controller.delete_category(category_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 