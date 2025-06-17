from fastapi import APIRouter, HTTPException
from app.schemas.external_server import ExternalServerCreate, ExternalServerOut
from app.schemas.category import CategoryCreate, CategoryOut
from app.services.admin_service import AdminService
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/external-server", response_model=ExternalServerOut)
def add_external_server(server: ExternalServerCreate):
    service = AdminService()
    try:
        return service.add_external_server(server)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/external-server/{server_id}/api-key", response_model=ExternalServerOut)
def update_server_api_key(server_id: int, api_key: str):
    service = AdminService()
    server = service.update_server_api_key(server_id, api_key)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

@router.get("/external-servers", response_model=List[ExternalServerOut])
def get_all_servers():
    service = AdminService()
    return service.get_all_servers()

@router.get("/external-server/{server_id}", response_model=ExternalServerOut)
def get_server(server_id: int):
    service = AdminService()
    server = service.get_server(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return server

@router.post("/category", response_model=CategoryOut)
def add_category(category: CategoryCreate):
    service = AdminService()
    try:
        return service.add_category(category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 