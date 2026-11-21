
from uuid import uuid4


class Category:

    def __init__(self, name, description="", category_id=None):
        self.category_id = category_id or str(uuid4())
        self.name = name
        self.description = description

        self._validate()

    def _validate(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Category name cannot be empty.")

        if not isinstance(self.description, str):
            raise ValueError("Description must be text.")

    def update_details(self, name=None, description=None):
        new_name = self.name if name is None else name
        new_description = (
            self.description if description is None else description
        )

        if not isinstance(new_name, str) or not new_name.strip():
            raise ValueError("Category name cannot be empty.")

        if not isinstance(new_description, str):
            raise ValueError("Description must be text.")

        self.name = new_name
        self.description = new_description

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            category_id=data["category_id"],
            name=data["name"],
            description=data["description"]
        )

    def __str__(self):
        return f"{self.name} - {self.description}"
