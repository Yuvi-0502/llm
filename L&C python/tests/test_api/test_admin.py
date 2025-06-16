import pytest
from fastapi import status

def test_get_external_servers_admin(client, test_admin):
    # First login to get token
    login_response = client.post(
        "/api/v1/login",
        data={"username": test_admin.email, "password": "adminpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Test getting external servers
    response = client.get(
        "/api/v1/admin/servers",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_get_external_servers_unauthorized(client, test_user):
    # First login to get token
    login_response = client.post(
        "/api/v1/login",
        data={"username": test_user.email, "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Test getting external servers as non-admin
    response = client.get(
        "/api/v1/admin/servers",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_create_external_server(client, test_admin):
    # First login to get token
    login_response = client.post(
        "/api/v1/login",
        data={"username": test_admin.email, "password": "adminpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Test creating external server
    server_data = {
        "name": "Test News API",
        "api_key": "test-api-key",
        "base_url": "https://test-api.com/news",
        "is_active": True
    }
    response = client.post(
        "/api/v1/admin/servers",
        json=server_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == server_data["name"]
    assert data["api_key"] == server_data["api_key"]
    assert data["base_url"] == server_data["base_url"]
    assert data["is_active"] == server_data["is_active"]

def test_update_external_server(client, test_admin, db):
    # First login to get token
    login_response = client.post(
        "/api/v1/login",
        data={"username": test_admin.email, "password": "adminpassword"}
    )
    token = login_response.json()["access_token"]
    
    # Create a test server
    from app.models.models import ExternalServer
    server = ExternalServer(
        name="Test News API",
        api_key="test-api-key",
        base_url="https://test-api.com/news",
        is_active=True
    )
    db.add(server)
    db.commit()
    db.refresh(server)
    
    # Test updating external server
    update_data = {
        "name": "Updated Test News API",
        "api_key": "updated-api-key",
        "is_active": False
    }
    response = client.put(
        f"/api/v1/admin/servers/{server.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["api_key"] == update_data["api_key"]
    assert data["is_active"] == update_data["is_active"]
    assert data["base_url"] == server.base_url  # Should remain unchanged 