from ..config.database import DbConnection
import mysql.connector as sql

class DbUtils:
    def db_query(self, query, params=None):
        try:
            connection = DbConnection.get_db_connection()
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params or ())
                    if query.strip().upper().startswith("SELECT"):
                        return cursor.fetchall()
                    connection.commit()
                    return cursor.rowcount
        except sql.Error as e:
            print(f"Database error: {e}")
            return None
