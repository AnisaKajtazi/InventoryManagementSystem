"""Dialog for adding and editing inventory products."""
import tkinter as tk
from tkinter import ttk

from models.item import Item


class ProductDialog(tk.Toplevel):
    def __init__(self, parent, categories, item=None):
        super().__init__(parent)
        self.title("Edit Product" if item else "Add Product")
        self.resizable(False, False)
        self.result = None
        self.transient(parent)
        self.grab_set()
        self.configure(padx=22, pady=18, bg="white")
        categories = list(categories)
        self.category_ids = {f"{c.name} ({c.category_id[:8]})": c.category_id for c in categories}
        fields = [("Product name", "name", item.name if item else ""),
                  ("Description", "description", item.description if item else ""),
                  ("Price", "price", str(item.price) if item else ""),
                  ("Quantity", "quantity", str(item.quantity) if item else "0"),
                  ("Low-stock threshold", "threshold", str(item.low_stock_threshold) if item else "5")]
        self.entries = {}
        for row, (label, key, value) in enumerate(fields):
            tk.Label(self, text=label, bg="white", fg="#243b5a",
                     font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", pady=6)
            entry = ttk.Entry(self, width=38)
            entry.insert(0, value)
            entry.grid(row=row, column=1, sticky="ew", pady=6)
            self.entries[key] = entry
        row = len(fields)
        tk.Label(self, text="Category", bg="white", fg="#243b5a",
                 font=("Segoe UI", 9, "bold")).grid(row=row, column=0, sticky="w", pady=6)
        self.category = ttk.Combobox(self, state="readonly", width=35,
                                     values=list(self.category_ids))
        self.category.grid(row=row, column=1, sticky="ew", pady=6)
        selected = next((key for key, value in self.category_ids.items()
                         if item and value == item.category_id), "")
        if selected:
            self.category.set(selected)
        elif self.category_ids:
            self.category.current(0)
        buttons = ttk.Frame(self)
        buttons.grid(row=row + 1, column=0, columnspan=2, sticky="e", pady=(16, 0))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text="Save product", command=lambda: self._submit(item)).pack(side="right")
        self.bind("<Return>", lambda _event: self._submit(item))
        self.entries["name"].focus_set()

    def _submit(self, item):
        try:
            category_id = self.category_ids.get(self.category.get())
            if not category_id:
                raise ValueError("Please select a category. Add a category first if none are available.")
            values = {
                "name": self.entries["name"].get().strip(),
                "description": self.entries["description"].get().strip(),
                "price": self.entries["price"].get().strip(),
                "quantity": int(self.entries["quantity"].get().strip()),
                "category_id": category_id,
                "low_stock_threshold": int(self.entries["threshold"].get().strip()),
            }
            if item:
                values["item_id"] = item.item_id
            self.result = Item(**values)
        except (ValueError, TypeError) as error:
            from tkinter import messagebox
            messagebox.showerror("Invalid product", str(error), parent=self)
            return
        self.destroy()
