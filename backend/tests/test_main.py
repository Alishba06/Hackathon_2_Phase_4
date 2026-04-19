import pytest
from fastapi.testclient import TestClient
from src.main import app
from sqlmodel import create_engine
from sqlmodel.pool import StaticPool
from src.config.database import SQLModel
from unittest.mock import patch

# Create a test client with an in-memory database
@pytest.fixture(name="client")
def fixture_client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    
    with TestClient(app) as client:
        yield client

# Mock JWT verification for testing
@patch("src.middleware.jwt_middleware.JWTBearer.__call__")
def test_read_root(mock_jwt):
    """Test the root endpoint"""
    mock_jwt.return_value = "fake_token"
    
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to the Todo API"}

def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}