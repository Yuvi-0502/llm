"""
API Client for making HTTP requests to the News Aggregation Server
"""

import requests
import json
from typing import Dict, Optional, Any
from client.config.config import API_BASE_URL, API_TIMEOUT


class APIClient:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
        self.session = requests.Session()
        self.token = None

    def set_token(self, token: str):
        """Set authentication token"""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_token(self):
        """Clear authentication token"""
        self.token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     params: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to the API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, params=params, timeout=self.timeout)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=self.timeout)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, timeout=self.timeout)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, timeout=self.timeout)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}

            # Try to parse JSON response
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = {"message": response.text}

            # Add status code to response
            response_data["status_code"] = response.status_code
            
            return response_data

        except requests.exceptions.ConnectionError:
            return {"error": "Connection failed. Please check if the server is running.", "status_code": 0}
        except requests.exceptions.Timeout:
            return {"error": "Request timed out.", "status_code": 0}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}", "status_code": 0}

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login user"""
        data = {"email": email, "password": password}
        response = self._make_request("POST", "/auth/login", data=data)
        
        if response.get("status_code") == 200 and "access_token" in response:
            self.set_token(response["access_token"])
        
        return response

    def register(self, username: str, email: str, password: str, role: str = "user") -> Dict[str, Any]:
        """Register new user"""
        data = {
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }
        return self._make_request("POST", "/auth/register", data=data)

    def logout(self) -> Dict[str, Any]:
        """Logout user"""
        response = self._make_request("POST", "/user/logout")
        self.clear_token()
        return response

    def get_news_status(self) -> Dict[str, Any]:
        """Get news system status"""
        return self._make_request("GET", "/news/status")

    def fetch_news(self) -> Dict[str, Any]:
        """Fetch news from external APIs"""
        return self._make_request("POST", "/news/fetch")

    def get_today_headlines(self, category: Optional[str] = None, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Get today's headlines"""
        params = {"page": page, "limit": limit}
        if category:
            params["category"] = category
        return self._make_request("GET", "/user/headlines/today", params=params)

    def get_headlines_by_date_range(self, start_date: str, end_date: str, category: Optional[str] = None, 
                                   page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Get headlines for a date range"""
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "page": page,
            "limit": limit
        }
        if category:
            params["category"] = category
        return self._make_request("GET", "/user/headlines/date-range", params=params)

    def search_articles(self, query: str, start_date: Optional[str] = None, end_date: Optional[str] = None,
                       sort_by: str = "published_at", page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Search articles"""
        params = {
            "query": query,
            "sort_by": sort_by,
            "page": page,
            "limit": limit
        }
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        return self._make_request("GET", "/user/search", params=params)

    def get_saved_articles(self, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Get saved articles"""
        params = {"page": page, "limit": limit}
        return self._make_request("GET", "/user/saved-articles", params=params)

    def save_article(self, article_id: int) -> Dict[str, Any]:
        """Save an article"""
        params = {"article_id": article_id}
        return self._make_request("POST", "/user/saved-articles", params=params)

    def delete_saved_article(self, article_id: int) -> Dict[str, Any]:
        """Delete a saved article"""
        return self._make_request("DELETE", f"/user/saved-articles/{article_id}")

    def get_categories(self) -> Dict[str, Any]:
        """Get all categories"""
        return self._make_request("GET", "/user/categories")

    def get_articles_by_category(self, category: str, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """Get articles by category"""
        params = {"page": page, "limit": limit}
        return self._make_request("GET", f"/user/categories/{category}/articles", params=params)

    def get_article_by_id(self, article_id: int) -> Dict[str, Any]:
        """Get specific article by ID"""
        return self._make_request("GET", f"/user/articles/{article_id}")

    # Admin endpoints
    def get_external_servers(self) -> Dict[str, Any]:
        """Get external servers (admin only)"""
        return self._make_request("GET", "/external-servers")

    def update_external_server(self, server_id: int, api_key: str) -> Dict[str, Any]:
        """Update external server API key (admin only)"""
        data = {"api_key": api_key}
        return self._make_request("PUT", f"/external-servers/{server_id}", data=data)

    def create_category(self, category_name: str) -> Dict[str, Any]:
        """Create new category (admin only)"""
        data = {"category_name": category_name}
        return self._make_request("POST", "/categories", data=data) 