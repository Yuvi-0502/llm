from server.core.database_connection import get_db_connection

class CategoryRepo:
    def find_category(self, category_name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM category WHERE category_name = %s", (category_name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def create_category(self, category_name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO category (category_name) VALUES (%s)", (category_name,))
        conn.commit()
        cursor.close()
        conn.close()
        return self.find_category(category_name)

    def get_by_name(self, name: str):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM category WHERE category_name = %s", (name,))
        category = cursor.fetchone()
        cursor.close()
        conn.close()
        return category

    def get_id_by_name(self, name: str):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT category_id FROM category WHERE category_name = %s", (name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

    def insert_article_category(self, category_id, article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO article_category_mapping(category_id, article_id) VALUES (%s,%s)", (category_id, article_id))
        conn.commit()
        cursor.close()
        conn.close()

    def ensure_default_categories_exist(self):
        """Ensure all default categories from CategoryClassifier exist in the database"""
        from server.utils.category_classifier import CategoryClassifier
        
        default_categories = list(CategoryClassifier.CATEGORY_KEYWORDS.keys()) + [CategoryClassifier.DEFAULT_CATEGORY]
        
        for category_name in default_categories:
            existing = self.get_by_name(category_name)
            if not existing:
                print(f"Creating default category: {category_name}")
                self.create_category(category_name)

    # def get_all(self):
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM category ORDER BY category_id")
    #     categories = cursor.fetchall()
    #     cursor.close()
    #     conn.close()
    #     return categories
    #
    # def get_by_id(self, category_id: int):
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM category WHERE category_id = %s", (category_id,))
    #     category = cursor.fetchone()
    #     cursor.close()
    #     conn.close()
    #     return category
    #
    # def update(self, category_id: int, name: str = None, description: str = None):
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
    #
    #     update_fields = []
    #     values = []
    #
    #     if name is not None:
    #         update_fields.append("name = %s")
    #         values.append(name)
    #
    #     if description is not None:
    #         update_fields.append("description = %s")
    #         values.append(description)
    #
    #     if update_fields:
    #         values.append(category_id)
    #         query = f"UPDATE category SET {', '.join(update_fields)} WHERE category_id = %s"
    #         cursor.execute(query, values)
    #         conn.commit()
    #
    #     cursor.close()
    #     conn.close()
    #     return self.get_by_id(category_id)
    #
    # def delete(self, category_id: int):
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("DELETE FROM category WHERE category_id = %s", (category_id,))
    #     conn.commit()
    #     cursor.close()
    #     conn.close()
    #     return True
