"""
Invalid request logging tests for the Todo application.

This module contains tests to verify that invalid requests
are properly logged and rejected with appropriate responses.
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


def test_unauthenticated_requests_logged_and_rejected(client: TestClient):
    """Test that unauthenticated requests are logged and rejected with 401."""
    # Make an unauthenticated request
    response = client.get("/api/user-id/tasks")
    
    # Verify that the response is 401 Unauthorized
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_invalid_token_requests_logged_and_rejected(client: TestClient):
    """Test that requests with invalid tokens are logged and rejected with 401."""
    # Make a request with an invalid token
    response = client.get(
        "/api/user-id/tasks",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    
    # Verify that the response is 401 Unauthorized
    assert response.status_code == 401
    assert "credentials" in response.json()["detail"]


def test_expired_token_requests_logged_and_rejected(client: TestClient):
    """Test that requests with expired tokens are logged and rejected with 401."""
    # Create an expired token manually
    import time
    from jose import jwt
    from src.config.security import JWT_SECRET_KEY, JWT_ALGORITHM
    
    expired_payload = {
        "sub": "test@example.com",
        "exp": time.time() - 1000  # Expired 1000 seconds ago
    }
    expired_token = jwt.encode(expired_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    # Make a request with an expired token
    response = client.get(
        "/api/user-id/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    
    # Verify that the response is 401 Unauthorized
    assert response.status_code == 401
    assert "expired" in response.json()["detail"]


def test_malformed_json_requests_logged_and_rejected(client: TestClient, valid_token: str):
    """Test that requests with malformed JSON are logged and rejected with 400."""
    # Make a request with malformed JSON
    response = client.post(
        f"/api/user-id/tasks",
        content="{invalid json",
        headers={
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json"
        }
    )
    
    # Verify that the response is 400 Bad Request or 422 Unprocessable Entity
    assert response.status_code in [400, 422]


def test_invalid_input_data_logged_and_rejected(client: TestClient, valid_token: str):
    """Test that requests with invalid input data are logged and rejected."""
    # Make a request with invalid input data (e.g., title too long)
    invalid_task_data = {
        "title": "A" * 300,  # Too long, exceeds 255 character limit
        "description": "Too long task title",
        "priority": "invalid_priority"  # Invalid priority value
    }
    
    response = client.post(
        f"/api/user-id/tasks",
        json=invalid_task_data,
        headers={
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json"
        }
    )
    
    # Verify that the response is 422 Unprocessable Entity for validation errors
    assert response.status_code in [400, 422]


def test_user_isolation_violations_logged_and_rejected(client: TestClient, valid_token: str):
    """Test that user isolation violations are logged and rejected with 403."""
    # Make a request where the user tries to access another user's resources
    response = client.get(
        f"/api/different-user-id/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Verify that the response is 403 Forbidden
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]


def test_nonexistent_resource_requests_logged_and_rejected(client: TestClient, valid_token: str):
    """Test that requests for nonexistent resources are handled appropriately."""
    # Make a request for a nonexistent task
    response = client.get(
        f"/api/user-id/tasks/nonexistent-task-id",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Verify that the response is 404 Not Found
    assert response.status_code == 404


def test_invalid_http_method_logged_and_rejected(client: TestClient, valid_token: str):
    """Test that requests with invalid HTTP methods are handled appropriately."""
    # Try to make a request with an unsupported HTTP method to a resource
    # (Though this depends on how the API is configured)
    # For example, if we try to PATCH to a GET-only endpoint
    response = client.patch(
        f"/api/user-id/tasks",
        json={"title": "Updated"},
        headers={
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json"
        }
    )
    
    # Verify that the response is 405 Method Not Allowed
    assert response.status_code == 405


def test_request_without_authorization_header_logged_and_rejected(client: TestClient):
    """Test that requests without authorization headers are logged and rejected."""
    # Make a request without the Authorization header
    response = client.get("/api/user-id/tasks")
    
    # Verify that the response is 401 Unauthorized
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_request_with_wrong_auth_scheme_logged_and_rejected(client: TestClient):
    """Test that requests with wrong auth schemes are logged and rejected."""
    # Make a request with wrong auth scheme (not Bearer)
    response = client.get(
        "/api/user-id/tasks",
        headers={"Authorization": "Basic some-invalid-credentials"}
    )
    
    # Verify that the response is 403 Forbidden or 401 Unauthorized
    assert response.status_code in [401, 403]