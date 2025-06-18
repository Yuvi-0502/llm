from fastapi import HTTPException
from services.external_server_service import ExternalServerService
from schemas.external_server import ExternalServerCreate, ExternalServerUpdate
from Exceptions.exceptions import ExternalServerNotFoundException
from config.http_status_code import HTTP_INTERNAL_SERVER_ERROR, HTTP_NOT_FOUND
from typing import List

class ExternalServerController:
    def __init__(self):
        self.service = ExternalServerService()

    def get_all_servers(self) -> List[dict]:
        try:
            return self.service.get_all_servers()
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_server_by_id(self, server_id: int) -> dict:
        try:
            return self.service.get_server_by_id(server_id)
        except ExternalServerNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def create_server(self, server: ExternalServerCreate) -> dict:
        try:
            return self.service.create_server(server)
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def update_server(self, server_id: int, server: ExternalServerUpdate) -> dict:
        try:
            return self.service.update_server(server_id, server)
        except ExternalServerNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete_server(self, server_id: int):
        try:
            self.service.delete_server(server_id)
            return {"message": f"Server {server_id} deleted successfully"}
        except ExternalServerNotFoundException as e:
            raise HTTPException(status_code=HTTP_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_active_servers(self) -> List[dict]:
        try:
            return self.service.get_active_servers()
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))
