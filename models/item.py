
from uuid import uuid4
from decimal import Decimal, InvalidOperation


class Item:

    def __init__(
        self,
        name,
        description,
        price,
        quantity,
        category_id,
        low_stock_threshold=5,
        item_id=None
    ):
        self.item_id = item_id or str(uuid4())

        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.category_id = category_id
        self.low_stock_threshold = low_stock_threshold

        self._validate()

    def _validate(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Product name cannot be empty.")

        if not isinstance(self.description, str):
            raise ValueError("Description must be text.")

        if not isinstance(self.category_id, str) or not self.category_id.strip():
            raise ValueError("Category ID is required.")

        try:
            self.price = Decimal(str(self.price))
        except (InvalidOperation, ValueError):
            raise ValueError("Price must be a valid number.")

        if not self.price.is_finite() or self.price < 0:
            raise ValueError("Price cannot be negative or invalid.")

        if type(self.quantity) is not int or self.quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")

        if (
            type(self.low_stock_threshold) is not int
            or self.low_stock_threshold < 0
        ):
            raise ValueError("Stock threshold must be a non-negative integer.")

    def update_details(
        self,
        name=None,
        description=None,
        price=None,
        category_id=None,
        low_stock_threshold=None
    ):
        new_name = self.name if name is None else name
        new_description = self.description if description is None else description
        new_price = self.price if price is None else price
        new_category_id = self.category_id if category_id is None else category_id
        new_threshold = (
            self.low_stock_threshold
            if low_stock_threshold is None
            else low_stock_threshold
        )

        old_values = (
            self.name,
            self.description,
            self.price,
            self.category_id,
            self.low_stock_threshold
        )

        self.name = new_name
        self.description = new_description
        self.price = new_price
        self.category_id = new_category_id
        self.low_stock_threshold = new_threshold

        try:
            self._validate()
        except ValueError:
            (
                self.name,
                self.description,
                self.price,
                self.category_id,
                self.low_stock_threshold
            ) = old_values
            raise

    def increase_stock(self, amount):
        if type(amount) is not int or amount <= 0:
            raise ValueError("Amount must be a positive integer.")

        self.quantity += amount

    def decrease_stock(self, amount):
        if type(amount) is not int or amount <= 0:
            raise ValueError("Amount must be a positive integer.")

        if amount > self.quantity:
            raise ValueError("Not enough stock available.")

        self.quantity -= amount

    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "quantity": self.quantity,
            "category_id": self.category_id,
            "low_stock_threshold": self.low_stock_threshold
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            item_id=data["item_id"],
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"],
            category_id=data["category_id"],
            low_stock_threshold=data["low_stock_threshold"]
        )

    def __str__(self):
        return (
            f"{self.name} | "
            f"Price: {self.price} | "
            f"Quantity: {self.quantity}"
        )
