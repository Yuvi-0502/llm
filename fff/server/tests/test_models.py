import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.article import Article
from app.models.external_api import ExternalAPI
from app.core.security import get_password_hash

def test_create_user(db: Session):
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
    
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.role == "USER"
    assert user.is_active is True

def test_create_article(db: Session):
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
    
    assert article.id is not None
    assert article.title == "Test Article"
    assert article.category == "GENERAL"

def test_create_external_api(db: Session):
    api = ExternalAPI(
        name="Test API",
        base_url="http://test-api.com",
        api_key="test-key",
        is_active=True
    )
    db.add(api)
    db.commit()
    db.refresh(api)
    
    assert api.id is not None
    assert api.name == "Test API"
    assert api.base_url == "http://test-api.com"
    assert api.is_active is True 