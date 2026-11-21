
from models.item import Item
from models.category import Category
from models.restock import Restock
from decimal import Decimal


class Inventory:
    """
    Main service class responsible for managing
    products, categories, stock and restock history.
    """

    def __init__(self, items=None, categories=None, restock_history=None):

        self.items = {
            item.item_id: item
            for item in (items or [])
        }

        self.categories = {
            category.category_id: category
            for category in (categories or [])
        }

        self.restock_history = list(restock_history or [])

    # ==========================================
    # PRODUCT MANAGEMENT
    # ==========================================

    def add_item(self, item):
        """Add a new product to the inventory."""

        if not isinstance(item, Item):
            raise TypeError("Expected an Item object.")

        if item.item_id in self.items:
            raise ValueError("Product already exists.")

        if item.category_id not in self.categories:
            raise ValueError("Category does not exist.")

        self.items[item.item_id] = item

        return item

    def get_item(self, item_id):
        """Get a product using its ID."""

        return self.items.get(item_id)

    def get_all_items(self):
        """Return all products."""

        return list(self.items.values())

    def update_item(self, item_id, **kwargs):
        """Update the details of an existing product."""

        item = self.get_item(item_id)

        if item is None:
            raise ValueError("Product not found.")

        new_category_id = kwargs.get("category_id")

        if (
            new_category_id is not None
            and new_category_id not in self.categories
        ):
            raise ValueError("Category does not exist.")

        item.update_details(**kwargs)

        return item

    def delete_item(self, item_id):
        """Delete a product from the inventory."""

        item = self.get_item(item_id)

        if item is None:
            raise ValueError("Product not found.")

        # Preserve historical restock records.
        if any(
            restock.item_id == item_id
            for restock in self.restock_history
        ):
            raise ValueError(
                "Cannot delete a product with restock history."
            )

        del self.items[item_id]

        return True

    def search_items(self, search_term):
        """Search products by name or description."""

        if not isinstance(search_term, str):
            raise TypeError("Search term must be text.")

        search_term = search_term.strip().lower()

        if not search_term:
            return self.get_all_items()

        return [
            item
            for item in self.items.values()
            if (
                search_term in item.name.lower()
                or search_term in item.description.lower()
            )
        ]

    # ==========================================
    # CATEGORY MANAGEMENT
    # ==========================================

    def add_category(self, category):
        """Add a new category."""

        if not isinstance(category, Category):
            raise TypeError("Expected a Category object.")

        if category.category_id in self.categories:
            raise ValueError("Category already exists.")

        for existing_category in self.categories.values():
            if existing_category.name.strip().lower() == category.name.strip().lower():
                raise ValueError("Category name already exists.")

        self.categories[category.category_id] = category

        return category

    def get_category(self, category_id):
        """Get a category using its ID."""

        return self.categories.get(category_id)

    def get_all_categories(self):
        """Return all categories."""

        return list(self.categories.values())

    def update_category(self, category_id, **kwargs):
        """Update an existing category."""

        category = self.get_category(category_id)

        if category is None:
            raise ValueError("Category not found.")

        new_name = kwargs.get("name")

        if new_name is not None:
            for existing_category in self.categories.values():

                if existing_category.category_id == category_id:
                    continue

                if existing_category.name.strip().lower() == new_name.strip().lower():
                    raise ValueError("Category name already exists.")

        category.update_details(**kwargs)

        return category

    def delete_category(self, category_id):
        """Delete a category if no products use it."""

        category = self.get_category(category_id)

        if category is None:
            raise ValueError("Category not found.")

        for item in self.items.values():
            if item.category_id == category_id:
                raise ValueError(
                    "Cannot delete a category that contains products."
                )

        del self.categories[category_id]

        return True

    def get_items_by_category(self, category_id):
        """Return all products belonging to a category."""

        if category_id not in self.categories:
            raise ValueError("Category not found.")

        return [
            item
            for item in self.items.values()
            if item.category_id == category_id
        ]

    # ==========================================
    # STOCK MANAGEMENT
    # ==========================================

    def increase_stock(self, item_id, amount):
        """Increase the stock quantity of a product."""

        item = self.get_item(item_id)

        if item is None:
            raise ValueError("Product not found.")

        item.increase_stock(amount)

        return item.quantity

    def decrease_stock(self, item_id, amount):
        """Decrease the stock quantity of a product."""

        item = self.get_item(item_id)

        if item is None:
            raise ValueError("Product not found.")

        item.decrease_stock(amount)

        return item.quantity

    def get_low_stock_items(self):
        """Return products that have low stock."""

        return [
            item
            for item in self.items.values()
            if item.is_low_stock()
        ]

    def get_inventory_summary(self):
        """Return general inventory statistics."""

        total_products = len(self.items)
        total_categories = len(self.categories)

        total_stock_units = sum(
            item.quantity
            for item in self.items.values()
        )

        low_stock_count = len(self.get_low_stock_items())

        total_inventory_value = sum(
            (
                item.price * item.quantity
                for item in self.items.values()
            ),
            start=Decimal("0")
        )

        return {
            "total_products": total_products,
            "total_categories": total_categories,
            "total_stock_units": total_stock_units,
            "low_stock_count": low_stock_count,
            "total_inventory_value": total_inventory_value
        }

    # ==========================================
    # RESTOCK MANAGEMENT
    # ==========================================

    def restock_item(self, item_id, quantity_added):
        """Restock a product and record the transaction."""

        item = self.get_item(item_id)

        if item is None:
            raise ValueError("Product not found.")

        # Create a new restock record.
        restock = Restock(
            item_id=item_id,
            quantity_added=quantity_added
        )

        # Increase the product stock.
        item.increase_stock(quantity_added)

        # Save the restock record in history.
        self.restock_history.append(restock)

        return restock

    def get_restock_history(self, item_id=None):
        """Return all restock records or records for one product."""

        if item_id is not None and item_id not in self.items:
            raise ValueError("Product not found.")

        history = self.restock_history

        if item_id is not None:
            history = [
                restock
                for restock in history
                if restock.item_id == item_id
            ]

        return sorted(
            history,
            key=lambda restock: restock.timestamp,
            reverse=True
        )

    # ==========================================
    # DATA CONVERSION
    # ==========================================

    def to_dict(self):
        """Convert the entire inventory into dictionaries."""

        return {
            "items": [
                item.to_dict()
                for item in self.items.values()
            ],

            "categories": [
                category.to_dict()
                for category in self.categories.values()
            ],

            "restock_history": [
                restock.to_dict()
                for restock in self.restock_history
            ]
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Inventory object from dictionary data."""

        items = [
            Item.from_dict(item_data)
            for item_data in data.get("items", [])
        ]

        categories = [
            Category.from_dict(category_data)
            for category_data in data.get("categories", [])
        ]

        restock_history = [
            Restock.from_dict(restock_data)
            for restock_data in data.get("restock_history", [])
        ]

        return cls(
            items=items,
            categories=categories,
            restock_history=restock_history
        )
