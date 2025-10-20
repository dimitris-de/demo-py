from src.services.item_service import ItemService


class TestItemService:
    """Tests for ItemService."""

    def test_get_item_with_query(self) -> None:
        """Test get_item with query parameter."""
        result = ItemService.get_item(42, "test")
        assert result["item_id"] == 42
        assert result["query"] == "test"
        assert result["name"] == "Item 42"

    def test_get_item_without_query(self) -> None:
        """Test get_item without query parameter."""
        result = ItemService.get_item(1)
        assert result["item_id"] == 1
        assert result["query"] is None
        assert result["name"] == "Item 1"

    def test_create_item(self) -> None:
        """Test create_item."""
        result = ItemService.create_item(99, "Test Item")
        assert result["item_id"] == 99
        assert result["name"] == "Test Item"
        assert result["created"] is True
