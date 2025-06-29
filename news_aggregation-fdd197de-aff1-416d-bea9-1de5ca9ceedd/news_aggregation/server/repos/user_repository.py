from server.core.database_connection import get_db_connection
from server.utils.password_utils import hash_password
class UserRepository:

    def get_user_by_email(self, email: str):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    def create(self, user):
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed_password = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (username, email, password, user_role) VALUES (%s, %s, %s, %s)",
            (user.username, user.email, hashed_password, user.role)
        )
        conn.commit()
        cursor.close()
        conn.close()
        # Return the created user (fetch again)
        return self.get_user_by_email(user.email)