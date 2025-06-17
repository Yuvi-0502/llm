import requests
from client.config import API_BASE_URL

class APIClient:
    def __init__(self):
        self.token = None
        self.user_role = None
        self.email = None

    def set_token(self, token):
        self.token = token

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    def register(self, username, email, password):
        data = {"username": username, "email": email, "password": password}
        resp = requests.post(f"{API_BASE_URL}/users/register", json=data)
        return resp

    def login(self, email, password):
        data = {"username": email, "password": password}
        resp = requests.post(f"{API_BASE_URL}/auth/login", data=data)
        if resp.ok:
            self.token = resp.json()["access_token"]
            # Decode JWT to get user role and email
            import jwt
            payload = jwt.decode(self.token, options={"verify_signature": False})
            self.user_role = payload.get("role")
            self.email = payload.get("sub")
        return resp

    def get_articles(self):
        resp = requests.get(f"{API_BASE_URL}/articles/", headers=self._headers())
        return resp

    def get_articles_by_category(self, category_id):
        resp = requests.get(f"{API_BASE_URL}/articles/?category_id={category_id}", headers=self._headers())
        return resp

    def get_articles_by_date(self, date):
        resp = requests.get(f"{API_BASE_URL}/articles/?date={date}", headers=self._headers())
        return resp

    def get_categories(self):
        resp = requests.get(f"{API_BASE_URL}/categories/", headers=self._headers())
        return resp

    def save_article(self, article_id):
        data = {"article_id": article_id}
        resp = requests.post(f"{API_BASE_URL}/users/saved-articles", json=data, headers=self._headers())
        return resp

    def get_saved_articles(self):
        resp = requests.get(f"{API_BASE_URL}/users/saved-articles", headers=self._headers())
        return resp

    def delete_saved_article(self, saved_id):
        resp = requests.delete(f"{API_BASE_URL}/users/saved-articles/{saved_id}", headers=self._headers())
        return resp

    def search_articles(self, query, start_date=None, end_date=None):
        params = {"q": query}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        resp = requests.get(f"{API_BASE_URL}/articles/search", params=params, headers=self._headers())
        return resp

    def get_notifications(self):
        resp = requests.get(f"{API_BASE_URL}/notifications/user/me", headers=self._headers())
        return resp

    def configure_notification(self, category_id, is_enabled):
        data = {"category_id": category_id, "is_enabled": is_enabled}
        resp = requests.post(f"{API_BASE_URL}/users/notifications/configure", json=data, headers=self._headers())
        return resp

    def add_keyword(self, keyword):
        data = {"keyword_name": keyword}
        resp = requests.post(f"{API_BASE_URL}/users/keywords", json=data, headers=self._headers())
        return resp

    # Admin methods
    def get_external_servers(self):
        resp = requests.get(f"{API_BASE_URL}/admin/external-servers", headers=self._headers())
        return resp

    def get_external_server_details(self, server_id):
        resp = requests.get(f"{API_BASE_URL}/admin/external-server/{server_id}", headers=self._headers())
        return resp

    def update_external_server_api_key(self, server_id, api_key):
        resp = requests.put(f"{API_BASE_URL}/admin/external-server/{server_id}/api-key?api_key={api_key}", headers=self._headers())
        return resp

    def add_category(self, category_name):
        data = {"category_name": category_name}
        resp = requests.post(f"{API_BASE_URL}/admin/category", json=data, headers=self._headers())
        return resp 