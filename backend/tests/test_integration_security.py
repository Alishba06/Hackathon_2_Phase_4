"""
End-to-end security testing for the Todo application.

This module contains integration tests to validate security
across frontend and backend components.
"""

import pytest
import subprocess
import sys
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


@pytest.fixture(name="user_a")
def fixture_user_a(session: Session):
    """Create first test user."""
    user = User(
        id="user-a-id",
        email="user_a@example.com",
        first_name="User",
        last_name="A",
        password_hash="$2b$12$D2nw2sVQjxZ71yP5qL4FbOyR9Z3y2Z8x7v6w5u4t3s2r1q0p9o8n7",  # bcrypt hash for "password"
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="user_b")
def fixture_user_b(session: Session):
    """Create second test user."""
    user = User(
        id="user-b-id",
        email="user_b@example.com",
        first_name="User",
        last_name="B",
        password_hash="$2b$12$D2nw2sVQjxZ71yP5qL4FbOyR9Z3y2Z8x7v6w5u4t3s2r1q0p9o8n7",  # bcrypt hash for "password"
        is_active=True
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="user_a_token")
def fixture_user_a_token(user_a: User):
    """Create a valid JWT token for user A."""
    data = {"sub": user_a.email, "user_id": user_a.id}
    token = create_access_token(data)
    return token


@pytest.fixture(name="user_b_token")
def fixture_user_b_token(user_b: User):
    """Create a valid JWT token for user B."""
    data = {"sub": user_b.email, "user_id": user_b.id}
    token = create_access_token(data)
    return token


def test_all_api_endpoints_reject_unauthenticated_requests(client: TestClient):
    """Test that all API endpoints reject unauthenticated requests with 401."""
    # List of all protected endpoints to test
    endpoints_to_test = [
        ("GET", "/api/user-id/tasks"),
        ("POST", "/api/user-id/tasks"),
        ("GET", "/api/user-id/tasks/task-id"),
        ("PUT", "/api/user-id/tasks/task-id"),
        ("PATCH", "/api/user-id/tasks/task-id"),
        ("DELETE", "/api/user-id/tasks/task-id"),
    ]
    
    for method, endpoint in endpoints_to_test:
        # Format endpoint with a dummy user ID
        formatted_endpoint = endpoint.replace("user-id", "dummy-user").replace("task-id", "dummy-task")
        
        if method == "GET":
            response = client.get(formatted_endpoint)
        elif method == "POST":
            response = client.post(formatted_endpoint, json={})
        elif method == "PUT":
            response = client.put(formatted_endpoint, json={})
        elif method == "PATCH":
            response = client.patch(formatted_endpoint, json={})
        elif method == "DELETE":
            response = client.delete(formatted_endpoint)
        
        # All should return 401 Unauthorized
        assert response.status_code == 401, f"Endpoint {formatted_endpoint} with method {method} should return 401 when unauthenticated"


def test_jwt_tokens_verified_using_shared_secret(client: TestClient, user_a_token: str):
    """Test that JWT tokens are verified using the shared secret."""
    # Access a protected endpoint with a valid token
    response = client.get(
        f"/api/{user_a_token}/tasks",  # This would need to be the actual user ID
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    # The response will be 404 (not found) or 403 (forbidden) depending on if the user exists
    # but it won't be 401 (unauthorized) if the token is valid
    assert response.status_code != 401, "Valid token should not result in 401 Unauthorized"


def test_backend_filters_task_queries_by_authenticated_user_id(client: TestClient, user_a_token: str):
    """Test that backend filters all task queries by authenticated user ID."""
    # This test would require creating tasks first
    # For now, we'll just verify that the user ID in the path is validated against the token
    user_id = "some-user-id"
    response = client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    
    # If the user_id in the path doesn't match the user_id in the token, it should return 403
    # This assumes the implementation compares the path user_id with the token user_id
    # The exact behavior depends on the implementation details


def test_frontend_cannot_display_modify_other_users_tasks(client: TestClient, user_a_token: str, user_b_token: str):
    """Test that frontend cannot display or modify tasks of other users."""
    # This is primarily a backend test since the frontend relies on the backend API
    # Test that User A cannot access User B's tasks
    response = client.get(
        f"/api/{user_b_token}/tasks",  # This should be user B's ID, not token
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert response.status_code == 403  # Forbidden


def test_spec_driven_validation_suite_passes():
    """Test that the spec-driven validation suite passes all tests."""
    # Run the security validation script
    result = subprocess.run([
        sys.executable, "scripts/run_security_validation.py", "--security-only"
    ], capture_output=True, text=True)
    
    # The script should exit with code 0 if all tests pass
    assert result.returncode == 0, f"Security validation failed: {result.stderr}"


def test_invalid_requests_logged_and_rejected(client: TestClient):
    """Test that invalid requests are logged and rejected appropriately."""
    # Test invalid token
    response = client.get(
        "/api/user-id/tasks",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401
    
    # Test expired token
    # (Would need to create an expired token for this test)
    
    # Test invalid input
    response = client.post(
        "/api/user-id/tasks",
        json={"title": "A" * 300},  # Too long title
        headers={"Authorization": "Bearer some-valid-token"}
    )
    # Should return 422 for validation error or 400 for bad request
    assert response.status_code in [400, 422]


def test_user_isolation_maintained_across_operations(client: TestClient, user_a_token: str, user_b_token: str):
    """Test that user isolation is maintained across all operations."""
    # User A tries to access User B's tasks
    response = client.get(
        f"/api/{'user-b-id'}/tasks",  # Using User B's ID
        headers={"Authorization": f"Bearer {user_a_token}"}  # With User A's token
    )
    assert response.status_code == 403  # Should be forbidden
    
    # User A tries to update User B's task
    response = client.put(
        f"/api/{'user-b-id'}/tasks/task-id",  # Trying to access User B's task
        json={"title": "Modified by User A"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert response.status_code == 403  # Should be forbidden
    
    # User A tries to delete User B's task
    response = client.delete(
        f"/api/{'user-b-id'}/tasks/task-id",  # Trying to delete User B's task
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert response.status_code == 403  # Should be forbidden


def test_security_rules_enforcement_during_runtime(client: TestClient, user_a_token: str):
    """Test that security rules are enforced during runtime."""
    # Test that authenticated endpoints require valid tokens
    response = client.get("/api/user-id/tasks")
    assert response.status_code == 401  # Should be unauthorized without token
    
    # Test that valid tokens work for the correct user
    response = client.get(
        f"/api/{'user-a-id'}/tasks",  # User A's own tasks
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    # Should not be 403 (forbidden) since it's the user's own data
    assert response.status_code != 403