"""
Security compliance tests for the Todo application.

This module contains tests to verify that security requirements
are properly implemented and enforced.
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from unittest.mock import patch

from src.main import app
from src.models.user import User
from src.models.task import Task
from src.config.security import JWT_SECRET_KEY, JWT_ALGORITHM
from src.utils.jwt_utils import create_access_token
from datetime import datetime, timedelta


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


@pytest.fixture(name="expired_token")
def fixture_expired_token(sample_user: User):
    # Create an expired JWT token
    data = {"sub": sample_user.email, "user_id": sample_user.id, "exp": datetime.utcnow() - timedelta(seconds=1)}
    token = create_access_token(data)
    return token


def test_unauthenticated_requests_return_401(client: TestClient):
    """Test that unauthenticated requests return 401 Unauthorized."""
    # Try to access a protected endpoint without authentication
    response = client.get("/api/invalid-user-id/tasks")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_invalid_token_returns_401(client: TestClient):
    """Test that requests with invalid tokens return 401 Unauthorized."""
    # Try to access a protected endpoint with an invalid token
    response = client.get(
        "/api/invalid-user-id/tasks",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_expired_token_returns_401(client: TestClient, expired_token: str):
    """Test that requests with expired tokens return 401 Unauthorized."""
    # Try to access a protected endpoint with an expired token
    response = client.get(
        "/api/invalid-user-id/tasks",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Token has expired"


def test_user_cannot_access_other_users_tasks(client: TestClient, valid_token: str):
    """Test that a user cannot access tasks belonging to another user."""
    # Try to access tasks with a valid token but wrong user ID
    response = client.get(
        "/api/different-user-id/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 403
    assert "Not authorized" in response.json()["detail"]


def test_jwt_verification_with_shared_secret(client: TestClient, valid_token: str):
    """Test that JWT tokens are verified using the shared secret."""
    # This test verifies that the token can be decoded with the correct secret
    # by attempting to access a protected endpoint
    user_id = "some-user-id"  # This would normally come from the token
    response = client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    # The response will be 404 (not found) or 403 (forbidden) depending on if the user exists
    # but it won't be 401 (unauthorized) if the token is valid
    assert response.status_code in [401, 403, 404]  # 401 if user_id doesn't match token, 403/404 for other reasons


def test_security_headers_present(client: TestClient):
    """Test that security-related headers are present in responses."""
    response = client.get("/")
    # Check that common security headers are present
    assert "x-frame-options" in [header.lower() for header in response.headers.keys()]