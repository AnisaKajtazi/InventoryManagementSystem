"""Product search, filtering, and CRUD view."""
import tkinter as tk
from tkinter import ttk, messagebox

from ui.common import BG, BLUE, MUTED, make_table, clear_table
from ui.dialogs.product_dialogs import ProductDialog


class ProductsView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        toolbar = tk.Frame(self, bg=BG)
        toolbar.pack(fill="x", pady=(0, 14))
        self.search = ttk.Entry(toolbar, width=30)
        self.search.pack(side="left", ipady=5)
        self.search.insert(0, "Search name or description")
        self.search.bind("<KeyRelease>", lambda _e: self.refresh())
        self.category_filter = ttk.Combobox(toolbar, state="readonly", width=23)
        self.category_filter.pack(side="left", padx=8)
        self.category_filter.bind("<<ComboboxSelected>>", lambda _e: self.refresh())
        self.status_filter = ttk.Combobox(toolbar, state="readonly", width=16,
                                          values=("All stock", "Low stock", "In stock"))
        self.status_filter.current(0)
        self.status_filter.pack(side="left")
        self.status_filter.bind("<<ComboboxSelected>>", lambda _e: self.refresh())
        ttk.Button(toolbar, text="Clear", command=self.clear_filters).pack(side="left", padx=7)
        ttk.Button(toolbar, text="＋ Add product", style="Primary.TButton",
                   command=self.add_product).pack(side="right")
        frame, self.table = make_table(self, ("id", "name", "category", "description", "price", "qty", "status"),
                                       ("ID", "Product", "Category", "Description", "Price", "Qty", "Status"),
                                       {"id": 90, "name": 160, "category": 125, "description": 240, "price": 85, "qty": 60, "status": 90})
        frame.pack(fill="both", expand=True)
        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=12)
        ttk.Button(actions, text="Edit selected", command=self.edit_product).pack(side="left")
        ttk.Button(actions, text="Delete selected", command=self.delete_product).pack(side="left", padx=8)
        self.table.bind("<Double-1>", lambda _e: self.edit_product())

    def clear_filters(self):
        self.search.delete(0, "end")
        self.category_filter.set("All categories")
        self.status_filter.current(0)
        self.refresh()

    def refresh(self):
        categories = self.app.inventory.get_all_categories()
        options = ["All categories"] + [c.name for c in categories]
        selected = self.category_filter.get()
        self.category_filter.configure(values=options)
        self.category_filter.set(selected if selected in options else "All categories")
        term = self.search.get().strip().lower()
        if term == "search name or description":
            term = ""
        category_id = next((c.category_id for c in categories if c.name == self.category_filter.get()), None)
        status = self.status_filter.get()
        clear_table(self.table)
        for item in self.app.inventory.get_all_items():
            if term and term not in item.name.lower() and term not in item.description.lower():
                continue
            if category_id and item.category_id != category_id:
                continue
            low = item.is_low_stock()
            if status == "Low stock" and not low or status == "In stock" and low:
                continue
            category = self.app.inventory.get_category(item.category_id)
            self.table.insert("", "end", iid=item.item_id, values=(item.item_id[:8], item.name,
                category.name if category else "Unknown", item.description, f"€{item.price:.2f}",
                item.quantity, "Low stock" if low else "In stock"), tags=("low",) if low else ())

    def _selected_item(self):
        selection = self.table.selection()
        if not selection:
            messagebox.showwarning("Select a product", "Choose a product first.", parent=self)
            return None
        return self.app.inventory.get_item(selection[0])

    def add_product(self):
        dialog = ProductDialog(self, self.app.inventory.get_all_categories())
        self.wait_window(dialog)
        if dialog.result:
            try:
                self.app.inventory.add_item(dialog.result)
                self.app.save()
            except (ValueError, TypeError) as error:
                messagebox.showerror("Could not add product", str(error), parent=self)

    def edit_product(self):
        item = self._selected_item()
        if not item:
            return
        dialog = ProductDialog(self, self.app.inventory.get_all_categories(), item)
        self.wait_window(dialog)
        if dialog.result:
            try:
                candidate = dialog.result
                self.app.inventory.update_item(item.item_id, name=candidate.name,
                    description=candidate.description, price=candidate.price,
                    category_id=candidate.category_id,
                    low_stock_threshold=candidate.low_stock_threshold,
                    quantity=candidate.quantity)
                self.app.save()
            except (ValueError, TypeError) as error:
                messagebox.showerror("Could not update product", str(error), parent=self)

    def delete_product(self):
        item = self._selected_item()
        if item and messagebox.askyesno("Delete product", f"Delete {item.name}? This cannot be undone.", parent=self):
            try:
                self.app.inventory.delete_item(item.item_id)
                self.app.save()
            except ValueError as error:
                messagebox.showerror("Could not delete product", str(error), parent=self)
