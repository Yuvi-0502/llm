from fastapi import APIRouter, Depends
from server.controller.external_server_controller import ExternalServerController
from server.core.jwt_utils import admin_required
from server.schemas.external_servers import ExternalServerUpdate

router = APIRouter(prefix="/external-servers", tags=["external_servers"])

@router.get("/all")
def get_all_external_servers(user=Depends(admin_required)):
    controller = ExternalServerController()
    return controller.get_all_servers()


@router.put("/{server_id}")
def update_server_details(server_id: int, server: ExternalServerUpdate, user= Depends(admin_required)):
    controller = ExternalServerController()
    return controller.update_server_details(server_id, server)
