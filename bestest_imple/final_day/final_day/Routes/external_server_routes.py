from fastapi import APIRouter, HTTPException, Depends
from schemas.external_server import ExternalServerCreate, ExternalServerUpdate, ExternalServerResponse
from controllers.external_server_controller import ExternalServerController
from Utils.jwt_handler import admin_required
from typing import List

router = APIRouter(prefix="/external-servers", tags=["external-servers"])

@router.get("/", response_model=List[ExternalServerResponse])
def get_all_servers(current_user=Depends(admin_required)):
    """Get all external servers (Admin only)"""
    try:
        controller = ExternalServerController()
        return controller.get_all_servers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{server_id}", response_model=ExternalServerResponse)
def get_server_by_id(server_id: int, current_user=Depends(admin_required)):
    """Get external server by ID (Admin only)"""
    try:
        controller = ExternalServerController()
        return controller.get_server_by_id(server_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/", response_model=ExternalServerResponse)
def create_server(server: ExternalServerCreate, current_user=Depends(admin_required)):
    """Create new external server (Admin only)"""
    try:
        controller = ExternalServerController()
        return controller.create_server(server)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{server_id}", response_model=ExternalServerResponse)
def update_server(server_id: int, server: ExternalServerUpdate, current_user=Depends(admin_required)):
    """Update external server (Admin only)"""
    try:
        controller = ExternalServerController()
        return controller.update_server(server_id, server)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{server_id}")
def delete_server(server_id: int, current_user=Depends(admin_required)):
    """Delete external server (Admin only)"""
    try:
        controller = ExternalServerController()
        return controller.delete_server(server_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/active/list")
def get_active_servers():
    """Get list of active external servers"""
    try:
        controller = ExternalServerController()
        return controller.get_active_servers()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
