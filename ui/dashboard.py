"""Inventory overview dashboard."""
import tkinter as tk
from tkinter import ttk

from ui.common import BG, card, make_table, clear_table


class DashboardView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self.cards = {}
        row = tk.Frame(self, bg=BG)
        row.pack(fill="x", pady=(0, 18))
        for key, label in (("total_products", "Products"), ("total_categories", "Categories"),
                           ("total_stock_units", "Stock units"), ("low_stock_count", "Low stock"),
                           ("total_inventory_value", "Inventory value")):
            panel, value = card(row, label, "—", "#b42318" if key == "low_stock_count" else "#1769aa")
            panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
            self.cards[key] = value
        content = tk.Frame(self, bg=BG)
        content.pack(fill="both", expand=True)
        left = tk.Frame(content, bg="white", padx=15, pady=12)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        tk.Label(left, text="Low stock products", bg="white", fg="#172b4d",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 10))
        frame, self.low_table = make_table(left, ("name", "quantity", "threshold"),
            ("Product", "Quantity", "Threshold"), {"name": 220, "quantity": 90, "threshold": 100}, 8)
        frame.pack(fill="both", expand=True)
        right = tk.Frame(content, bg="white", padx=15, pady=12)
        right.pack(side="right", fill="both", expand=True)
        tk.Label(right, text="Recent restocks", bg="white", fg="#172b4d",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 10))
        frame, self.recent_table = make_table(right, ("product", "added", "date"),
            ("Product", "Added", "Date"), {"product": 180, "added": 75, "date": 170}, 8)
        frame.pack(fill="both", expand=True)

    def refresh(self):
        summary = self.app.inventory.get_inventory_summary()
        for key, label in self.cards.items():
            value = summary[key]
            label.configure(text=f"€{value:,.2f}" if key == "total_inventory_value" else f"{value:,}")
        clear_table(self.low_table)
        for item in self.app.inventory.get_low_stock_items():
            self.low_table.insert("", "end", values=(item.name, item.quantity, item.low_stock_threshold), tags=("low",))
        clear_table(self.recent_table)
        for record in self.app.inventory.get_restock_history()[:8]:
            item = self.app.inventory.get_item(record.item_id)
            self.recent_table.insert("", "end", values=(item.name if item else "Deleted product",
                record.quantity_added, record.timestamp.replace("T", " ")))
