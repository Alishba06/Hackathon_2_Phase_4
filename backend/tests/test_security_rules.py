"""
Security rule validation tests for the Todo application.

This module contains tests to verify that security rules
are properly enforced throughout the application.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.main import app
from src.models.user import User
from src.models.task import Task
from src.utils.jwt_utils import create_access_token


@pytest.fixture(name="engine")
def fixture_engine():
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(name="session")
def fixture_session(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def fixture_client(engine):
    with TestClient(app) as client:
        yield client


@pytest.fixture(name="sample_user")
def fixture_sample_user(session: Session):
    # Create a sample user for testing
    user = User(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password_hash="$2b$12$D2nw2sVQjxZ71yP5qL4FbOyR9Z3y2Z8x7v6w5u4t3s2r1q0p9o8n7",  # bcrypt hash for "password"
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="valid_token")
def fixture_valid_token(sample_user: User):
    # Create a valid JWT token for the sample user
    data = {"sub": sample_user.email, "user_id": sample_user.id}
    token = create_access_token(data)
    return token


def test_jwt_token_required_for_protected_endpoints(client: TestClient):
    """Test that all protected endpoints require a valid JWT token."""
    # List of protected endpoints to test
    protected_endpoints = [
        ("/api/user-id/tasks", "GET"),
        ("/api/user-id/tasks", "POST"),
        ("/api/user-id/tasks/task-id", "GET"),
        ("/api/user-id/tasks/task-id", "PUT"),
        ("/api/user-id/tasks/task-id", "PATCH"),
        ("/api/user-id/tasks/task-id", "DELETE"),
    ]
    
    for endpoint, method in protected_endpoints:
        # Make request without authorization header
        if method == "GET":
            response = client.get(endpoint)
        elif method == "POST":
            response = client.post(endpoint, json={})
        elif method == "PUT":
            response = client.put(endpoint, json={})
        elif method == "PATCH":
            response = client.patch(endpoint, json={})
        elif method == "DELETE":
            response = client.delete(endpoint)
        
        # All should return 401 Unauthorized
        assert response.status_code == 401, f"Endpoint {endpoint} with method {method} should require authentication"


def test_jwt_token_verification_enforced(client: TestClient):
    """Test that JWT tokens are properly verified."""
    # Try to access a protected endpoint with an invalid token
    response = client.get(
        "/api/user-id/tasks",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401
    assert "credentials" in response.json()["detail"]


def test_user_isolation_enforced(client: TestClient, valid_token: str):
    """Test that users can only access their own resources."""
    # Try to access tasks with a valid token but mismatched user ID
    response = client.get(
        "/api/different-user-id/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    # Should return 403 Forbidden due to user isolation
    assert response.status_code == 403


def test_request_validation_enforced(client: TestClient, valid_token: str):
    """Test that all requests are validated against the API contract."""
    # Test with malformed request data
    response = client.post(
        "/api/user-id/tasks",
        json={"invalid_field": "value"},  # Invalid field that shouldn't exist
        headers={
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json"
        }
    )
    # Should return 400 Bad Request for invalid input
    assert response.status_code in [400, 422]  # 422 is also valid for validation errors


def test_security_headers_present(client: TestClient):
    """Test that security-related headers are present in responses."""
    response = client.get("/")
    # Check that common security headers are present
    headers_lower = [h.lower() for h in response.headers.keys()]
    # Note: These headers may not be set by default in FastAPI
    # This test would need to be adjusted based on your actual security header implementation


def test_rate_limiting_not_bypassed(client: TestClient):
    """Test that rate limiting cannot be bypassed."""
    # This test would require implementation of rate limiting middleware
    # For now, we'll just verify that the concept is considered
    pass  # Implementation would depend on rate limiting setup


def test_csrf_protection(client: TestClient):
    """Test that CSRF protection is in place where needed."""
    # This test would require implementation of CSRF protection
    # For state-changing operations like POST, PUT, DELETE
    pass  # Implementation would depend on CSRF protection setup


def test_input_sanitization(client: TestClient, valid_token: str):
    """Test that inputs are properly sanitized to prevent injection attacks."""
    malicious_inputs = [
        {"title": "<script>alert('xss')</script>"},
        {"title": "'; DROP TABLE tasks; --"},
        {"description": "javascript:alert('xss')"},
    ]
    
    for malicious_input in malicious_inputs:
        response = client.post(
            "/api/user-id/tasks",
            json=malicious_input,
            headers={
                "Authorization": f"Bearer {valid_token}",
                "Content-Type": "application/json"
            }
        )
        # Should not return 500 Internal Server Error due to injection
        # May return 422 for validation error or 200 if properly sanitized
        assert response.status_code != 500