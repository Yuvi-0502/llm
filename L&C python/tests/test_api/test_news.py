import pytest
from fastapi import status
from datetime import datetime, timedelta

def test_get_news_by_category(client, test_user):
    # First login to get token
    login_response = client.post(
        "/api/v1/login",
        data={"username": test_user.email, "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Test getting news by category
    response = client.get(
        "/api/v1/news/category/business",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_search_news(client, test_user):
    # First login to get token
    login_response = client.post(
        "/api/v1/login",
        data={"username": test_user.email, "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Test searching news
    response = client.get(
        "/api/v1/news/search?query=test",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_save_article(client, test_user, db):
    # First login to get token
    login_response = client.post(
        "/api/v1/login",
        data={"username": test_user.email, "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Create a test article
    from app.models.models import NewsArticle
    article = NewsArticle(
        title="Test Article",
        description="Test Description",
        content="Test Content",
        url="http://test.com",
        source="Test Source",
        category="business",
        published_at=datetime.utcnow()
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    
    # Test saving article
    response = client.post(
        f"/api/v1/news/save/{article.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Article saved successfully"

def test_get_saved_articles(client, test_user, db):
    # First login to get token
    login_response = client.post(
        "/api/v1/login",
        data={"username": test_user.email, "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Create a test article
    from app.models.models import NewsArticle
    article = NewsArticle(
        title="Test Article",
        description="Test Description",
        content="Test Content",
        url="http://test.com",
        source="Test Source",
        category="business",
        published_at=datetime.utcnow()
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    
    # Save the article for the test user
    test_user.saved_articles.append(article)
    db.commit()
    
    # Test getting saved articles
    response = client.get(
        "/api/v1/news/saved",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Test Article" 