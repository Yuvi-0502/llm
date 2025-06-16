import requests
from typing import Optional, Dict, Any, List
from app.core.config import get_settings

settings = get_settings()


class APIClient:
    def __init__(self):
        self.base_url = settings.API_URL
        self.token: Optional[str] = None

    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login to the API"""
        response = requests.post(
            f"{self.base_url}/auth/login",
            data={"username": email, "password": password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data["access_token"]
        return data

    def signup(self, username: str, email: str, password: str) -> Dict[str, Any]:
        """Sign up a new user"""
        response = requests.post(
            f"{self.base_url}/auth/signup",
            json={"username": username, "email": email, "password": password}
        )
        response.raise_for_status()
        return response.json()

    def get_headlines(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get news headlines"""
        params = {}
        if category:
            params["category"] = category
        
        response = requests.get(
            f"{self.base_url}/articles/headlines",
            headers=self._get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_saved_articles(self) -> List[Dict[str, Any]]:
        """Get user's saved articles"""
        response = requests.get(
            f"{self.base_url}/articles/saved",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def save_article(self, article_id: int) -> Dict[str, Any]:
        """Save an article"""
        response = requests.post(
            f"{self.base_url}/articles/{article_id}/save",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def delete_saved_article(self, article_id: int) -> Dict[str, Any]:
        """Delete a saved article"""
        response = requests.delete(
            f"{self.base_url}/articles/{article_id}/save",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def search_articles(self, query: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search articles"""
        params = {"query": query}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        response = requests.get(
            f"{self.base_url}/articles/search",
            headers=self._get_headers(),
            params=params
        )
        response.raise_for_status()
        return response.json()

    def get_notifications(self) -> List[Dict[str, Any]]:
        """Get user's notifications"""
        response = requests.get(
            f"{self.base_url}/notifications",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def update_notification_preferences(self, preferences: Dict[str, bool]) -> Dict[str, Any]:
        """Update notification preferences"""
        response = requests.put(
            f"{self.base_url}/notifications/preferences",
            headers=self._get_headers(),
            json=preferences
        )
        response.raise_for_status()
        return response.json()

    def add_keyword(self, keyword: str) -> Dict[str, Any]:
        """Add a keyword for notifications"""
        response = requests.post(
            f"{self.base_url}/notifications/keywords",
            headers=self._get_headers(),
            json={"keyword": keyword}
        )
        response.raise_for_status()
        return response.json()

    def remove_keyword(self, keyword: str) -> Dict[str, Any]:
        """Remove a keyword"""
        response = requests.delete(
            f"{self.base_url}/notifications/keywords/{keyword}",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    # Admin endpoints
    def get_external_servers(self) -> List[Dict[str, Any]]:
        """Get list of external servers (admin only)"""
        response = requests.get(
            f"{self.base_url}/external-servers",
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json()

    def update_external_server(self, server_id: int, api_key: str) -> Dict[str, Any]:
        """Update external server details (admin only)"""
        response = requests.put(
            f"{self.base_url}/external-servers/{server_id}",
            headers=self._get_headers(),
            json={"api_key": api_key}
        )
        response.raise_for_status()
        return response.json()

    def add_category(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Add a new category (admin only)"""
        response = requests.post(
            f"{self.base_url}/categories",
            headers=self._get_headers(),
            json={"name": name, "description": description}
        )
        response.raise_for_status()
        return response.json() 