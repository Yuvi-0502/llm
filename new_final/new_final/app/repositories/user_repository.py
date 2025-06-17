from app.core.database import get_db_connection

class UserRepository:
    def get_by_email(self, email: str):
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
        cursor.execute(
            "INSERT INTO users (username, email, password, user_role) VALUES (%s, %s, %s, %s)",
            (user.username, user.email, user.password, "user")
        )
        conn.commit()
        cursor.close()
        conn.close()
        # Return the created user (fetch again)
        return self.get_by_email(user.email) 