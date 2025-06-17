from app.core.database import get_db_connection
from app.schemas.category import CategoryCreate

class CategoryRepository:
    def get(self, category_id: int):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category WHERE category_id = %s", (category_id,))
        category = cursor.fetchone()
        cursor.close()
        conn.close()
        return category

    def get_by_name(self, name: str):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category WHERE category_name = %s", (name,))
        category = cursor.fetchone()
        cursor.close()
        conn.close()
        return category

    def get_all(self):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return categories

    def create(self, category: CategoryCreate):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO category (category_name) VALUES (%s)",
            (category.category_name,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return self.get_by_name(category.category_name) 