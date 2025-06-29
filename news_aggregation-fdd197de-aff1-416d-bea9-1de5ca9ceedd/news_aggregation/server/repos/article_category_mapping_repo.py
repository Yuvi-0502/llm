from server.core.database_connection import get_db_connection

class CategoryArticleMappingRepo:
    def create_article_category_mapping(self, category_id, article_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO category_article_mapping (category_id, article_id) VALUES (%s, %s)",
            (category_id, article_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
