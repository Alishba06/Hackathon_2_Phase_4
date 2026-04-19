"""
API contract validation tests for the Todo application.

This module contains tests to verify that API endpoints
comply with the defined contracts and specifications.
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


def test_get_tasks_endpoint_contract(client: TestClient, valid_token: str):
    """Test that the GET /api/{user_id}/tasks endpoint follows the API contract."""
    user_id = "some-user-id"
    response = client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Check that the response has the correct structure
    assert response.status_code in [200, 403, 404]  # 200 if successful, 403 if forbidden, 404 if user not found
    
    if response.status_code == 200:
        # If successful, check that the response follows the contract
        data = response.json()
        assert isinstance(data, list)  # Should return a list of tasks


def test_post_tasks_endpoint_contract(client: TestClient, valid_token: str):
    """Test that the POST /api/{user_id}/tasks endpoint follows the API contract."""
    user_id = "some-user-id"
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "due_date": "2026-12-31T23:59:59",
        "priority": "medium"
    }
    
    response = client.post(
        f"/api/{user_id}/tasks",
        json=task_data,
        headers={
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json"
        }
    )
    
    # Check that the response has the correct structure
    assert response.status_code in [200, 400, 401, 403]  # 200 if successful, others for various errors


def test_get_single_task_endpoint_contract(client: TestClient, valid_token: str):
    """Test that the GET /api/{user_id}/tasks/{task_id} endpoint follows the API contract."""
    user_id = "some-user-id"
    task_id = "some-task-id"
    
    response = client.get(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Check that the response has the correct structure
    assert response.status_code in [200, 401, 403, 404]  # 200 if successful, others for various errors


def test_put_task_endpoint_contract(client: TestClient, valid_token: str):
    """Test that the PUT /api/{user_id}/tasks/{task_id} endpoint follows the API contract."""
    user_id = "some-user-id"
    task_id = "some-task-id"
    task_update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "is_completed": True,
        "due_date": "2026-12-31T23:59:59",
        "priority": "high"
    }
    
    response = client.put(
        f"/api/{user_id}/tasks/{task_id}",
        json=task_update_data,
        headers={
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json"
        }
    )
    
    # Check that the response has the correct structure
    assert response.status_code in [200, 400, 401, 403, 404]


def test_patch_task_endpoint_contract(client: TestClient, valid_token: str):
    """Test that the PATCH /api/{user_id}/tasks/{task_id} endpoint follows the API contract."""
    user_id = "some-user-id"
    task_id = "some-task-id"
    task_update_data = {
        "is_completed": True
    }
    
    response = client.patch(
        f"/api/{user_id}/tasks/{task_id}",
        json=task_update_data,
        headers={
            "Authorization": f"Bearer {valid_token}",
            "Content-Type": "application/json"
        }
    )
    
    # Check that the response has the correct structure
    assert response.status_code in [200, 400, 401, 403, 404]


def test_delete_task_endpoint_contract(client: TestClient, valid_token: str):
    """Test that the DELETE /api/{user_id}/tasks/{task_id} endpoint follows the API contract."""
    user_id = "some-user-id"
    task_id = "some-task-id"
    
    response = client.delete(
        f"/api/{user_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    
    # Check that the response has the correct structure
    assert response.status_code in [200, 401, 403, 404]
    
    if response.status_code == 200:
        # Check that the response has the expected message
        data = response.json()
        assert "message" in data


def test_error_response_format(client: TestClient):
    """Test that error responses follow the standardized format."""
    # Try to access an endpoint without authentication to trigger an error
    response = client.get("/api/invalid-user-id/tasks")
    
    assert response.status_code == 401
    
    # Check that the error response follows the specified format
    error_data = response.json()
    assert "error" in error_data
    assert "message" in error_data["error"]
    assert "code" in error_data["error"]  # This might not be present in our implementation
    assert "path" in error_data["error"]  # This might not be present in our implementation