from abc import ABC, abstractmethod

class ExternalAPIService(ABC):
    @abstractmethod
    def fetch_news_articles(self, server_config: dict):
        """
        Fetch news articles from the external API using the provided server configuration.
        Args:
            server_config (dict): Configuration for the external server (API URL, key, etc.)
        Returns:
            list: List of NewsArticleCreate or similar objects.
        """
        pass 