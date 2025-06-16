import os
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    def __init__(self):
        self.base_url = os.getenv("API_URL", "http://localhost:8000/api/v1")
        self.token = None

    def set_token(self, token: str):
        self.token = token

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            headers=self._get_headers(),
            json=data
        )
        response.raise_for_status()
        return response.json()

    # Auth endpoints
    def login(self, email: str, password: str) -> Dict:
        return self._make_request("POST", "/auth/login", {
            "email": email,
            "password": password
        })

    def signup(self, username: str, email: str, password: str) -> Dict:
        return self._make_request("POST", "/auth/signup", {
            "username": username,
            "email": email,
            "password": password
        })

    # News endpoints
    def get_news(self, category: Optional[str] = None) -> List[Dict]:
        params = {"category": category} if category else {}
        return self._make_request("GET", "/news", params)

    def search_news(self, query: str) -> List[Dict]:
        return self._make_request("GET", "/news/search", {"query": query})

    def save_article(self, article_id: int) -> Dict:
        return self._make_request("POST", f"/news/{article_id}/save")

    def get_saved_articles(self) -> List[Dict]:
        return self._make_request("GET", "/news/saved")

    # Admin endpoints
    def get_external_servers(self) -> List[Dict]:
        return self._make_request("GET", "/admin/external-servers")

    def create_external_server(self, data: Dict) -> Dict:
        return self._make_request("POST", "/admin/external-servers", data)

    def update_external_server(self, server_id: int, data: Dict) -> Dict:
        return self._make_request("PUT", f"/admin/external-servers/{server_id}", data)

    def delete_external_server(self, server_id: int) -> Dict:
        return self._make_request("DELETE", f"/admin/external-servers/{server_id}")

    # Notification endpoints
    def get_notification_preferences(self) -> Dict:
        return self._make_request("GET", "/notifications/preferences")

    def update_notification_preferences(self, data: Dict) -> Dict:
        return self._make_request("PUT", "/notifications/preferences", data) 