from server.core.database_connection import get_db_connection
from typing import List, Optional


class ExternalAPIRepository:
    def __init__(self):
        self.conn = get_db_connection()

    def  get_all_servers(self) -> List[dict]:
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM external_server")
        servers = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return servers

    def get_server_by_id(self, server_id: int) -> Optional[dict]:
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM external_server WHERE server_id = %s", (server_id,))
        server = cursor.fetchone()
        cursor.close()
        self.conn.close()
        return server

    def update_server_api_key(self, server_id: int, new_api_key: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE external_server SET api_key = %s, last_accessed = NOW() WHERE server_id = %s",
            (new_api_key, server_id)
        )
        self.conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        self.conn.close()
        return updated

    def update_last_accessed(self, server_id: int):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE external_server SET last_accessed = NOW() WHERE server_id = %s",
            (server_id,)
        )
        self.conn.commit()
        cursor.close()
        self.conn.close()
