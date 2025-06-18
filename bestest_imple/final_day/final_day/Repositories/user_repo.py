from config.database import DbConnection
from schemas.user import UserCreate
from Utils.password_utils import hash_password

class UserRepository:
    def get_by_email(self, email: str):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user

    def create(self, user: UserCreate):
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        hashed_password = hash_password(user.password)
        cursor.execute(
            "INSERT INTO users (user_name, email, password, role) VALUES (%s, %s, %s, %s)",
            (user.user_name, user.email, hashed_password, user.role)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return self.get_by_email(user.email)