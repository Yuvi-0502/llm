from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.models import Category, User
from app.schemas.category import CategoryResponse, CategoryCreate

router = APIRouter()


@router.get("/", response_model=List[CategoryResponse])
def get_categories(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all categories.
    """
    categories = db.query(Category).all()
    return categories


@router.post("/", response_model=CategoryResponse)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin_user),
    category_in: CategoryCreate,
) -> Any:
    """
    Create new category (admin only).
    """
    category = db.query(Category).filter(Category.name == category_in.name).first()
    if category:
        raise HTTPException(
            status_code=400,
            detail="Category with this name already exists"
        )
    
    category = Category(**category_in.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category 