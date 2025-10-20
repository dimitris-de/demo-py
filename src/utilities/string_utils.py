def sanitize_string(value: str) -> str:
    """
    Sanitize a string by stripping whitespace.

    Args:
        value: String to sanitize.

    Returns:
        Sanitized string.
    """
    return value.strip() if value else ""


def truncate_string(value: str, max_length: int = 100) -> str:
    """
    Truncate string to maximum length.

    Args:
        value: String to truncate.
        max_length: Maximum allowed length.

    Returns:
        Truncated string.
    """
    if len(value) <= max_length:
        return value
    return value[: max_length - 3] + "..."
