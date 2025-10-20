from src.utilities.string_utils import sanitize_string, truncate_string


class TestStringUtils:
    """Tests for string utility functions."""

    def test_sanitize_string_strips_whitespace(self) -> None:
        """Test sanitize_string removes leading/trailing whitespace."""
        assert sanitize_string("  hello  ") == "hello"
        assert sanitize_string("\n\tworld\n") == "world"

    def test_sanitize_string_handles_empty(self) -> None:
        """Test sanitize_string handles empty strings."""
        assert sanitize_string("") == ""
        assert sanitize_string("   ") == ""

    def test_truncate_string_within_limit(self) -> None:
        """Test truncate_string keeps short strings unchanged."""
        text = "Short text"
        assert truncate_string(text, 50) == text

    def test_truncate_string_exceeds_limit(self) -> None:
        """Test truncate_string truncates long strings."""
        text = "A" * 150
        result = truncate_string(text, 100)
        assert len(result) == 100
        assert result.endswith("...")
        assert result == "A" * 97 + "..."

    def test_truncate_string_exact_limit(self) -> None:
        """Test truncate_string at exact limit."""
        text = "A" * 100
        result = truncate_string(text, 100)
        assert result == text
