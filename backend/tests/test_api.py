"""
Basic tests for the API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "FSM SaaS Platform API"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_docs_accessible():
    """Test API documentation is accessible"""
    response = client.get("/api/v1/docs")
    assert response.status_code == 200


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "invalid@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401


def test_unauthorized_access():
    """Test accessing protected endpoint without authentication"""
    response = client.get("/api/v1/admin/dashboard")
    assert response.status_code == 401
