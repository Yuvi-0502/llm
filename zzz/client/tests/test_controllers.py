import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from app.controllers.auth_controller import AuthController
from app.controllers.article_controller import ArticleController
from app.controllers.admin_controller import AdminController
from app.models.user import User, UserRole
from app.models.article import Article, ArticleCategory
from app.models.external_api import ExternalAPI

@pytest.fixture
def mock_api_client():
    return Mock()

@pytest.fixture
def auth_controller(mock_api_client):
    return AuthController(mock_api_client)

@pytest.fixture
def article_controller(mock_api_client):
    return ArticleController(mock_api_client)

@pytest.fixture
def admin_controller(mock_api_client):
    return AdminController(mock_api_client)

def test_auth_controller_login(auth_controller, mock_api_client):
    mock_api_client.login.return_value = {"access_token": "test_token"}
    mock_api_client.get_user_profile.return_value = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "role": "USER",
        "is_active": True
    }
    
    with patch('builtins.input', side_effect=["testuser", "testpass"]):
        user = auth_controller.login()
        assert user is not None
        assert user.username == "testuser"
        assert user.role == UserRole.USER

def test_article_controller_get_today_articles(article_controller, mock_api_client):
    mock_api_client.get_today_articles.return_value = [{
        "id": 1,
        "title": "Test Article",
        "description": "Test Description",
        "content": "Test Content",
        "url": "http://test.com",
        "source_name": "Test Source",
        "author": "Test Author",
        "published_at": datetime.utcnow().isoformat(),
        "category": "GENERAL"
    }]
    
    with patch('builtins.input', return_value="q"):
        article_controller.get_today_articles()
        mock_api_client.get_today_articles.assert_called_once()

def test_admin_controller_get_external_apis(admin_controller, mock_api_client):
    mock_api_client.get_external_apis.return_value = [{
        "id": 1,
        "name": "Test API",
        "base_url": "http://test-api.com",
        "api_key": "test-key",
        "is_active": True
    }]
    
    admin_controller.current_user = User(
        id=1,
        username="admin",
        email="admin@example.com",
        role=UserRole.ADMIN,
        is_active=True
    )
    
    with patch('builtins.input', return_value="3"):
        admin_controller.get_external_apis()
        mock_api_client.get_external_apis.assert_called_once() 