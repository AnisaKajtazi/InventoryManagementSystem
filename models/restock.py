
from uuid import uuid4
from datetime import datetime


class Restock:

    def __init__(
        self,
        item_id,
        quantity_added,
        timestamp=None,
        restock_id=None
    ):
        self.restock_id = restock_id or str(uuid4())
        self.item_id = item_id
        self.quantity_added = quantity_added

        self.timestamp = (
            timestamp
            if timestamp is not None
            else datetime.now().isoformat(timespec="seconds")
        )

        self._validate()

    def _validate(self):
        if not isinstance(self.item_id, str) or not self.item_id.strip():
            raise ValueError("Item ID is required.")

        if type(self.quantity_added) is not int or self.quantity_added <= 0:
            raise ValueError("Restock quantity must be a positive integer.")

        if not isinstance(self.timestamp, str) or not self.timestamp.strip():
            raise ValueError("Timestamp is required.")

        try:
            datetime.fromisoformat(self.timestamp)
        except ValueError:
            raise ValueError("Invalid timestamp format.")

    def to_dict(self):
        return {
            "restock_id": self.restock_id,
            "item_id": self.item_id,
            "quantity_added": self.quantity_added,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            restock_id=data["restock_id"],
            item_id=data["item_id"],
            quantity_added=data["quantity_added"],
            timestamp=data["timestamp"]
        )

    def __str__(self):
        return (
            f"Restock: {self.quantity_added} units | "
            f"Date: {self.timestamp}"
        )
