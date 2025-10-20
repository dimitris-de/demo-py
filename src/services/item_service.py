import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ItemService:
    """Service for item-related operations."""

    @staticmethod
    def get_item(item_id: int, query: Optional[str] = None) -> Dict:
        """
        Retrieve item by ID.

        Args:
            item_id: The item identifier.
            query: Optional query parameter.

        Returns:
            Dict containing item information.
        """
        logger.info(f"Retrieving item {item_id} with query: {query}")
        return {"item_id": item_id, "query": query, "name": f"Item {item_id}"}

    @staticmethod
    def create_item(item_id: int, name: str) -> Dict:
        """
        Create a new item.

        Args:
            item_id: The item identifier.
            name: The item name.

        Returns:
            Dict containing created item information.
        """
        logger.info(f"Creating item {item_id} with name: {name}")
        return {"item_id": item_id, "name": name, "created": True}
