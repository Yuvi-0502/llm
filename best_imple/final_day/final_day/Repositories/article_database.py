from abc import ABC, abstractmethod
from Server.Models.article import Article
from typing import List


class ArticleDatabase(ABC):

    def insert(self, new_article: Article):
        pass

    def get_by_id(self, id: int):
        pass

    def update_by_id(self, id: int, new_article: Article):
        pass

    def delete_by_id(self, id: int):
        pass

    def get_all(self) -> List[Article]:
        pass

