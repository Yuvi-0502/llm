import pytest
from fastapi import status

def test_login_success(client, test_user):
    response = client.post(
        "/api/v1/login",
        data={"username": test_user.email, "password": "testpassword"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    response = client.post(
        "/api/v1/login",
        data={"username": test_user.email, "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_signup_success(client):
    response = client.post(
        "/api/v1/signup",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert "id" in data

def test_signup_existing_email(client, test_user):
    response = client.post(
        "/api/v1/signup",
        json={
            "username": "newuser",
            "email": test_user.email,
            "password": "newpassword"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_signup_existing_username(client, test_user):
    response = client.post(
        "/api/v1/signup",
        json={
            "username": test_user.username,
            "email": "newuser@example.com",
            "password": "newpassword"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST 