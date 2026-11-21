"""Category administration view."""
import tkinter as tk
from tkinter import ttk, messagebox

from ui.common import BG, make_table, clear_table
from ui.dialogs.category_dialogs import CategoryDialog


class CategoriesView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(0, 14))
        ttk.Button(bar, text="＋ Add category", style="Primary.TButton", command=self.add_category).pack(side="right")
        frame, self.table = make_table(self, ("id", "name", "description", "count"),
            ("Category ID", "Name", "Description", "Products"),
            {"id": 120, "name": 200, "description": 420, "count": 100})
        frame.pack(fill="both", expand=True)
        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=12)
        ttk.Button(actions, text="Edit selected", command=self.edit_category).pack(side="left")
        ttk.Button(actions, text="View products", command=self.view_products).pack(side="left", padx=8)
        ttk.Button(actions, text="Delete selected", command=self.delete_category).pack(side="left")

    def refresh(self):
        clear_table(self.table)
        for category in self.app.inventory.get_all_categories():
            count = len(self.app.inventory.get_items_by_category(category.category_id))
            self.table.insert("", "end", iid=category.category_id,
                values=(category.category_id[:8], category.name, category.description, count))

    def _selected(self):
        ids = self.table.selection()
        if not ids:
            messagebox.showwarning("Select a category", "Choose a category first.", parent=self)
            return None
        return self.app.inventory.get_category(ids[0])

    def add_category(self):
        dialog = CategoryDialog(self)
        self.wait_window(dialog)
        if dialog.result:
            try:
                self.app.inventory.add_category(dialog.result)
                self.app.save()
            except ValueError as error:
                messagebox.showerror("Could not add category", str(error), parent=self)

    def edit_category(self):
        category = self._selected()
        if not category:
            return
        dialog = CategoryDialog(self, category)
        self.wait_window(dialog)
        if dialog.result:
            try:
                self.app.inventory.update_category(category.category_id,
                    name=category.name, description=category.description)
                self.app.save()
            except ValueError as error:
                messagebox.showerror("Could not update category", str(error), parent=self)

    def delete_category(self):
        category = self._selected()
        if category and messagebox.askyesno("Delete category", f"Delete {category.name}?", parent=self):
            try:
                self.app.inventory.delete_category(category.category_id)
                self.app.save()
            except ValueError as error:
                messagebox.showerror("Could not delete category", str(error), parent=self)

    def view_products(self):
        category = self._selected()
        if category:
            products = self.app.inventory.get_items_by_category(category.category_id)
            text = "\n".join(f"• {item.name} — {item.quantity} units" for item in products) or "No products in this category."
            messagebox.showinfo(category.name, text, parent=self)
