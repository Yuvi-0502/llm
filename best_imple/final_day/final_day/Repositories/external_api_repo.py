from Server.config.database import DbConnection
from typing import Optional

class ExternalAPIRepository:
    def get_api_status(self):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            select * from external_server
            """
        )
        external_server_data = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return external_server_data

    def get_server_by_id(self, server_id: int) -> Optional[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM external_server WHERE server_id = %s", (server_id,))
        server = cursor.fetchone()
        cursor.close()
        conn.close()
        return server

    def update_server_api_key(self, server_id: int, new_api_key: str) -> bool:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE external_server SET api_key = %s, last_accessed = NOW() WHERE server_id = %s",
            (new_api_key, server_id)
        )
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return updated

    def update_last_accessed(self, server_id: int):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE external_server SET last_accessed = NOW() WHERE server_id = %s",
            (server_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()

