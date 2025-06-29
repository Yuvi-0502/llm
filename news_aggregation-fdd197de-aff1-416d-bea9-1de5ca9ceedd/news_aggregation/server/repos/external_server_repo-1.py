from server.core.database_connection import get_db_connection
from server.schemas.external_servers import ExternalServerUpdate
from datetime import datetime


class ExternalServerRepository:
    def get_all_servers(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM external_server ORDER BY server_id")
        servers = cursor.fetchall()
        cursor.close()
        conn.close()
        return servers

    def get_server_by_id(self, server_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM external_server WHERE server_id = %s", (server_id,))
        server = cursor.fetchone()
        cursor.close()
        conn.close()
        return server
    #
    # def create(self, server: ExternalServerCreate):
    #     conn = DbConnection.get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         "INSERT INTO external_servers (server_name, api_key, base_url) VALUES (%s, %s, %s)",
    #         (server.server_name, server.api_key, server.base_url)
    #     )
    #     conn.commit()
    #     server_id = cursor.lastrowid
    #     cursor.close()
    #     conn.close()
    #     return self.get_by_id(server_id)
    #
    def update_server_details(self, server_id: int, server: ExternalServerUpdate):
        conn = get_db_connection()
        cursor = conn.cursor()

        update_fields = []
        values = []

        if server.server_name is not None:
            update_fields.append("server_name = %s")
            values.append(server.server_name)

        if server.api_key is not None:
            update_fields.append("api_key = %s")
            values.append(server.api_key)

        if server.base_url is not None:
            update_fields.append("base_url = %s")
            values.append(server.base_url)

        if server.is_active is not None:
            update_fields.append("is_active = %s")
            values.append(server.is_active)

        if update_fields:
            update_fields.append("last_accessed = %s")
            values.append(datetime.now())
            values.append(server_id)

            query = f"UPDATE external_servers SET {', '.join(update_fields)} WHERE server_id = %s"
            cursor.execute(query, values)
            conn.commit()

        cursor.close()
        conn.close()
        return self.get_server_by_id(server_id)

    # def delete(self, server_id: int):
    #     conn = DbConnection.get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("DELETE FROM external_servers WHERE server_id = %s", (server_id,))
    #     conn.commit()
    #     cursor.close()
    #     conn.close()
    #
    # def get_active_servers(self):
    #     conn = DbConnection.get_db_connection()
    #     cursor = conn.cursor(dictionary=True)
    #     cursor.execute("SELECT * FROM external_servers WHERE is_active = TRUE")
    #     servers = cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    #     return servers
    #
    # def update_last_accessed(self, server_id: int):
    #     conn = DbConnection.get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         "UPDATE external_servers SET last_accessed = %s WHERE server_id = %s",
    #         (datetime.now(), server_id)
    #     )
    #     conn.commit()
    #     cursor.close()
    #     conn.close()