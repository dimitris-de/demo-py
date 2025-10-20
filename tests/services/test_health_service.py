from src.services.health_service import HealthService


class TestHealthService:
    """Tests for HealthService."""

    def test_get_health_status_returns_healthy(self) -> None:
        """Test health status returns healthy."""
        result = HealthService.get_health_status()
        assert result["status"] == "healthy"
        assert "python_version" in result
        assert "." in result["python_version"]

    def test_get_readiness_status_returns_ready(self) -> None:
        """Test readiness status returns ready."""
        result = HealthService.get_readiness_status()
        assert result["ready"] is True
