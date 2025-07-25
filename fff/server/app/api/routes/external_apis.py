from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.container import Container, get_container
from app.core.security import get_current_admin_user
from app.schemas.external_api import ExternalAPI, ExternalAPICreate, ExternalAPIUpdate
from app.schemas.user import User

router = APIRouter()

@router.get("/", response_model=List[ExternalAPI])
async def read_apis(
    skip: int = 0,
    limit: int = 100,
    is_active: bool = None,
    current_user: User = Depends(get_current_admin_user),
    container: Container = Depends(get_container)
):
    """Get all external APIs (admin only)."""
    return container.external_api_service.get_apis(
        skip=skip,
        limit=limit,
        is_active=is_active
    )

@router.get("/active", response_model=List[ExternalAPI])
async def read_active_apis(
    current_user: User = Depends(get_current_admin_user),
    container: Container = Depends(get_container)
):
    """Get all active external APIs (admin only)."""
    return container.external_api_service.get_active_apis()

@router.get("/{api_id}", response_model=ExternalAPI)
async def read_api(
    api_id: int,
    current_user: User = Depends(get_current_admin_user),
    container: Container = Depends(get_container)
):
    """Get external API by ID (admin only)."""
    api = container.external_api_service.get_api(api_id=api_id)
    if not api:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External API not found"
        )
    return api

@router.post("/", response_model=ExternalAPI)
async def create_api(
    api: ExternalAPICreate,
    current_user: User = Depends(get_current_admin_user),
    container: Container = Depends(get_container)
):
    """Create new external API (admin only)."""
    return container.external_api_service.create_api(api=api)

@router.put("/{api_id}", response_model=ExternalAPI)
async def update_api(
    api_id: int,
    api: ExternalAPIUpdate,
    current_user: User = Depends(get_current_admin_user),
    container: Container = Depends(get_container)
):
    """Update external API (admin only)."""
    updated_api = container.external_api_service.update_api(
        api_id=api_id,
        api=api
    )
    if not updated_api:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External API not found"
        )
    return updated_api

@router.delete("/{api_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api(
    api_id: int,
    current_user: User = Depends(get_current_admin_user),
    container: Container = Depends(get_container)
):
    """Delete external API (admin only)."""
    if not container.external_api_service.delete_api(api_id=api_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External API not found"
        ) 