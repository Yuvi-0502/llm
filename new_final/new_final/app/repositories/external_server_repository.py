from app.core.database import get_db_connection
from app.schemas.external_server import ExternalServerCreate

class ExternalServerRepository:
    def get(self, server_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM external_server WHERE server_id = %s", (server_id,))
        server = cursor.fetchone()
        cursor.close()
        conn.close()
        return server

    def get_by_name(self, name: str):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM external_server WHERE server_name = %s", (name,))
        server = cursor.fetchone()
        cursor.close()
        conn.close()
        return server

    def get_all(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM external_server")
        servers = cursor.fetchall()
        cursor.close()
        conn.close()
        return servers

    def create(self, server: ExternalServerCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO external_server (server_name, api_key, is_active, last_accessed) VALUES (%s, %s, %s, %s)",
            (server.server_name, server.api_key, server.is_active, server.last_accessed)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return self.get_by_name(server.server_name)

    def update_api_key(self, server_id: int, api_key: str):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE external_server SET api_key = %s WHERE server_id = %s", (api_key, server_id))
        conn.commit()
        cursor.close()
        conn.close()
        return self.get(server_id) 