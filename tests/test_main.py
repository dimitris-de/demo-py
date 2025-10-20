import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_returns_welcome_message(self, client: TestClient) -> None:
        """Test root endpoint returns welcome message."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Demo Python App" in data["message"]


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_health_check_returns_healthy_status(self, client: TestClient) -> None:
        """Test health check endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "python_version" in data

    def test_readiness_check_returns_ready_status(self, client: TestClient) -> None:
        """Test readiness check endpoint."""
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is True


class TestItemEndpoints:
    """Tests for item endpoints."""

    def test_read_item_with_query_parameter(self, client: TestClient) -> None:
        """Test item endpoint with query parameter."""
        response = client.get("/items/42?q=test")
        assert response.status_code == 200
        data = response.json()
        assert data["item_id"] == 42
        assert data["query"] == "test"

    def test_read_item_without_query_parameter(self, client: TestClient) -> None:
        """Test item endpoint without query parameter."""
        response = client.get("/items/1")
        assert response.status_code == 200
        data = response.json()
        assert data["item_id"] == 1
        assert data["query"] is None
