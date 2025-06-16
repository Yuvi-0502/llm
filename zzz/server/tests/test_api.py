import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.core.security import create_access_token
from app.models.user import User
from app.models.article import Article
from app.models.external_api import ExternalAPI
from app.core.security import get_password_hash

client = TestClient(app)

@pytest.fixture
def test_user(db):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass"),
        role="USER",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_admin(db):
    admin = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpass"),
        role="ADMIN",
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture
def test_article(db):
    article = Article(
        title="Test Article",
        description="Test Description",
        content="Test Content",
        url="http://test.com",
        source_name="Test Source",
        source_id="test123",
        author="Test Author",
        published_at=datetime.utcnow(),
        category="GENERAL"
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

def test_login(test_user):
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_articles(test_user):
    access_token = create_access_token({"sub": test_user.username})
    response = client.get(
        "/api/articles/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_article(test_user, test_article):
    access_token = create_access_token({"sub": test_user.username})
    response = client.get(
        f"/api/articles/{test_article.id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_article.title

def test_get_external_apis(test_admin):
    access_token = create_access_token({"sub": test_admin.username})
    response = client.get(
        "/api/external-apis/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_external_api(test_admin):
    access_token = create_access_token({"sub": test_admin.username})
    response = client.post(
        "/api/external-apis/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "New API",
            "base_url": "http://new-api.com",
            "api_key": "new-key",
            "description": "Test API"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New API"
    assert data["base_url"] == "http://new-api.com" 