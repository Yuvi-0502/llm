from fastapi import APIRouter, Depends
from server.schemas.category import CategoryCreate
from server.controller.category_controller import CategoryController
from server.core.jwt_utils import admin_required
# from typing import List

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/")
def add_category(category: CategoryCreate, user= Depends(admin_required)):
    controller = CategoryController()
    return controller.create_category(category)