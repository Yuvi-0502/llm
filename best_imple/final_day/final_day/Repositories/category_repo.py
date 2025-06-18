from config.database import DbConnection
from typing import List, Optional

class CategoryRepository:
    def get_all(self) -> List[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return categories

    def get_by_id(self, category_id: int) -> Optional[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
        category = cursor.fetchone()
        cursor.close()
        conn.close()
        return category

    def get_by_name(self, name: str) -> Optional[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories WHERE name = %s", (name,))
        category = cursor.fetchone()
        cursor.close()
        conn.close()
        return category

    def create(self, name: str, description: str = None) -> dict:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categories (name, description) VALUES (%s, %s)",
            (name, description)
        )
        conn.commit()
        category_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return self.get_by_id(category_id)

    def update(self, category_id: int, name: str = None, description: str = None) -> Optional[dict]:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        
        update_fields = []
        values = []
        
        if name is not None:
            update_fields.append("name = %s")
            values.append(name)
        
        if description is not None:
            update_fields.append("description = %s")
            values.append(description)
        
        if update_fields:
            values.append(category_id)
            query = f"UPDATE categories SET {', '.join(update_fields)} WHERE category_id = %s"
            cursor.execute(query, values)
            conn.commit()
        
        cursor.close()
        conn.close()
        return self.get_by_id(category_id)

    def delete(self, category_id: int) -> bool:
        conn = DbConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE category_id = %s", (category_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True 