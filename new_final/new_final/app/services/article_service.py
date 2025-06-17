from app.repositories.article_repository import ArticleRepository
from app.schemas.article import ArticleCreate

class ArticleService:
    def __init__(self):
        self.repo = ArticleRepository()

    def create_article(self, article: ArticleCreate):
        return self.repo.create(article)

    def get_article(self, article_id: int):
        return self.repo.get(article_id)

    def get_all_articles(self):
        return self.repo.get_all()

    def delete_article(self, article_id: int):
        return self.repo.delete(article_id) 