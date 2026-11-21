"""Reusable category creation and editing dialog."""
import tkinter as tk
from tkinter import ttk, messagebox

from models.category import Category


class CategoryDialog(tk.Toplevel):
    def __init__(self, parent, category=None):
        super().__init__(parent)
        self.title("Edit Category" if category else "Add Category")
        self.result = None
        self.transient(parent)
        self.grab_set()
        self.configure(padx=20, pady=18, bg="white")
        self.name = ttk.Entry(self, width=40)
        self.description = ttk.Entry(self, width=40)
        for row, (label, entry, value) in enumerate((
            ("Name", self.name, category.name if category else ""),
            ("Description", self.description, category.description if category else ""),
        )):
            tk.Label(self, text=label, bg="white", fg="#243b5a").grid(row=row, column=0, sticky="w", pady=7)
            entry.insert(0, value)
            entry.grid(row=row, column=1, pady=7)
        buttons = ttk.Frame(self)
        buttons.grid(row=2, column=0, columnspan=2, sticky="e", pady=(12, 0))
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text="Save category", command=lambda: self._submit(category)).pack(side="right")
        self.name.focus_set()

    def _submit(self, category):
        try:
            name, description = self.name.get().strip(), self.description.get().strip()
            if category:
                self.result = Category(name=name, description=description,
                                       category_id=category.category_id)
            else:
                self.result = Category(name=name, description=description)
        except ValueError as error:
            messagebox.showerror("Invalid category", str(error), parent=self)
            return
        self.destroy()
