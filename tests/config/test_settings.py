from src.config.settings import Settings


class TestSettings:
    """Tests for Settings configuration."""

    def test_settings_defaults(self) -> None:
        """Test default settings values."""
        settings = Settings()
        assert settings.app_name == "Demo Python App"
        assert settings.app_version == "0.1.0"
        assert settings.debug is False
        assert settings.host == "0.0.0.0"
        assert settings.port == 8000

    def test_settings_can_be_overridden(self) -> None:
        """Test settings can be overridden."""
        settings = Settings(app_name="Test App", debug=True)
        assert settings.app_name == "Test App"
        assert settings.debug is True
