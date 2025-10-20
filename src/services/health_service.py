import logging
import sys
from typing import Dict

logger = logging.getLogger(__name__)


class HealthService:
    """Service for health check operations."""

    @staticmethod
    def get_health_status() -> Dict[str, str]:
        """
        Get application health status.

        Returns:
            Dict containing health status and Python version.
        """
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        logger.debug(f"Health check performed: Python {python_version}")
        return {"status": "healthy", "python_version": python_version}

    @staticmethod
    def get_readiness_status() -> Dict[str, bool]:
        """
        Get application readiness status.

        Returns:
            Dict containing readiness status.
        """
        return {"ready": True}
