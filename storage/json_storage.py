
import json
from pathlib import Path


class JSONStorage:
    """
    Handles reading and writing inventory data
    using a JSON file.
    """

    def __init__(self, file_path=None):

        if file_path is None:
            self.file_path = Path(__file__).resolve().parent / "inventory.json"
        else:
            self.file_path = Path(file_path)

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def _get_empty_data(self):
        """Return the default empty inventory structure."""

        return {
            "items": [],
            "categories": [],
            "restock_history": []
        }

    def load_data(self):
        """
        Load inventory data from the JSON file.

        If the file does not exist, create it
        with an empty inventory structure.
        """

        if not self.file_path.exists():
            empty_data = self._get_empty_data()
            self.save_data(empty_data)
            return empty_data

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Invalid JSON file: {self.file_path}"
            ) from error

        if not isinstance(data, dict):
            raise ValueError("JSON data must be an object.")

        required_keys = [
            "items",
            "categories",
            "restock_history"
        ]

        for key in required_keys:
            if key not in data:
                raise ValueError(
                    f"Missing required section: {key}"
                )

            if not isinstance(data[key], list):
                raise ValueError(
                    f"The '{key}' section must be a list."
                )

        return data

    def save_data(self, data):
        """
        Save inventory data to the JSON file.

        Accepts either an Inventory object
        or a dictionary.
        """

        if hasattr(data, "to_dict") and callable(data.to_dict):
            data = data.to_dict()

        if not isinstance(data, dict):
            raise TypeError(
                "Data must be an Inventory object or dictionary."
            )

        required_keys = [
            "items",
            "categories",
            "restock_history"
        ]

        for key in required_keys:
            if key not in data or not isinstance(data[key], list):
                raise ValueError(
                    f"Invalid or missing section: {key}"
                )

        temp_file = self.file_path.with_suffix(".tmp")

        try:
            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            # Replace the original file after successful writing.
            temp_file.replace(self.file_path)

        except (OSError, TypeError, ValueError):
            if temp_file.exists():
                temp_file.unlink()
            raise
