from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...models.user import User
from ...models.external_api import ExternalAPI
from ...schemas.external_api import ExternalAPI as ExternalAPISchema, ExternalAPICreate, ExternalAPIUpdate
from ..deps import get_current_admin_user

router = APIRouter()

@router.get("/", response_model=List[ExternalAPISchema])
async def read_external_apis(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    apis = db.query(ExternalAPI).all()
    return apis

@router.get("/{api_id}", response_model=ExternalAPISchema)
async def read_external_api(
    *,
    db: Session = Depends(get_db),
    api_id: int,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    api = db.query(ExternalAPI).filter(ExternalAPI.id == api_id).first()
    if not api:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External API not found"
        )
    return api

@router.post("/", response_model=ExternalAPISchema)
async def create_external_api(
    *,
    db: Session = Depends(get_db),
    api_in: ExternalAPICreate,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    api = ExternalAPI(**api_in.dict())
    db.add(api)
    db.commit()
    db.refresh(api)
    return api

@router.put("/{api_id}", response_model=ExternalAPISchema)
async def update_external_api(
    *,
    db: Session = Depends(get_db),
    api_id: int,
    api_in: ExternalAPIUpdate,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    api = db.query(ExternalAPI).filter(ExternalAPI.id == api_id).first()
    if not api:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External API not found"
        )
    
    for field, value in api_in.dict(exclude_unset=True).items():
        setattr(api, field, value)
    
    db.add(api)
    db.commit()
    db.refresh(api)
    return api

@router.delete("/{api_id}")
async def delete_external_api(
    *,
    db: Session = Depends(get_db),
    api_id: int,
    current_user: User = Depends(get_current_admin_user),
) -> Any:
    api = db.query(ExternalAPI).filter(ExternalAPI.id == api_id).first()
    if not api:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="External API not found"
        )
    
    db.delete(api)
    db.commit()
    return {"message": "External API deleted successfully"} 