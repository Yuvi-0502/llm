from fastapi import HTTPException

from server.schemas.external_servers import ExternalServerUpdate
from server.services.external_server_service import ExternalServerService
# from schemas.external_server import ExternalServerCreate, ExternalServerUpdate
# from server.Exceptions.user_exceptions import ExternalServerNotFoundException
from server.config.http_status_codes import HTTP_INTERNAL_SERVER_ERROR
from typing import List

class ExternalServerController:
    def __init__(self):
        self.service = ExternalServerService()

    def get_all_servers(self) -> List[dict]:
        try:
            return self.service.get_all_servers()
        except Exception as e:
            raise HTTPException(status_code=HTTP_INTERNAL_SERVER_ERROR, detail=str(e))

    def update_server_details(self, server_id: int, server: ExternalServerUpdate):
        return self.service.update_server_details(server_id, server)