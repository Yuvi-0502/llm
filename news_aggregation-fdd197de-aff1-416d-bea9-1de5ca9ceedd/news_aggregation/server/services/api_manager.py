from server.repos.external_server_repo import ExternalServerRepository
from server.services.newsapi_service import NewsAPIService
from server.services.thenewsapi_service import TheNewsAPIService
from typing import List

class APIManager:
    SERVICE_CLASS_MAP = {
        "News API": NewsAPIService,
        "The News API": TheNewsAPIService,
        # Add more mappings as needed
    }

    def __init__(self):
        self.external_server_repo = ExternalServerRepository()

    def get_active_apis(self):
        apis = self.external_server_repo.get_all_servers()
        return [api for api in apis if api.get("is_active") in (1, True)]

    def get_all_server_details(self):
        return self.external_server_repo.get_all_servers()

    def fetch_news_from_all_active_servers(self) -> List:
        articles = []
        active_apis = self.get_active_apis()
        for api in active_apis:
            service_class = self.SERVICE_CLASS_MAP.get(api["server_name"])
            if not service_class:
                continue  # Unknown service, skip
            service = service_class()
            server_config = {
                "api_url": api["api_url"],
                "api_key": api["api_key"],
                "server_id": api["server_id"]
            }
            try:
                articles.extend(service.fetch_news_articles(server_config))
            except Exception as e:
                print(f"[APIManager] Error fetching from {api['server_name']}: {e}")
        return articles