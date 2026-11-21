"""Stock level monitoring and adjustments."""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from ui.common import BG, make_table, clear_table


class StockView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(0, 14))
        ttk.Button(bar, text="Increase stock", style="Primary.TButton",
                   command=lambda: self.adjust(1)).pack(side="left")
        ttk.Button(bar, text="Decrease stock", command=lambda: self.adjust(-1)).pack(side="left", padx=8)
        self.low_only = tk.BooleanVar(value=False)
        ttk.Checkbutton(bar, text="Show low stock only", variable=self.low_only,
                        command=self.refresh).pack(side="right")
        frame, self.table = make_table(self, ("name", "quantity", "threshold", "status"),
            ("Product", "Current quantity", "Low-stock threshold", "Status"),
            {"name": 260, "quantity": 150, "threshold": 180, "status": 130})
        frame.pack(fill="both", expand=True)

    def refresh(self):
        clear_table(self.table)
        for item in self.app.inventory.get_all_items():
            low = item.is_low_stock()
            if self.low_only.get() and not low:
                continue
            self.table.insert("", "end", iid=item.item_id,
                values=(item.name, item.quantity, item.low_stock_threshold,
                        "LOW STOCK" if low else "In stock"), tags=("low",) if low else ())

    def adjust(self, direction):
        ids = self.table.selection()
        if not ids:
            messagebox.showwarning("Select a product", "Choose a product to adjust.", parent=self)
            return
        amount = simpledialog.askinteger("Stock adjustment", "Quantity to " + ("add:" if direction > 0 else "remove:"),
                                         parent=self, minvalue=1)
        if amount is None:
            return
        try:
            if direction > 0:
                self.app.inventory.increase_stock(ids[0], amount)
            else:
                self.app.inventory.decrease_stock(ids[0], amount)
            self.app.save()
            messagebox.showinfo("Stock updated", "The stock quantity was updated.", parent=self)
        except ValueError as error:
            messagebox.showerror("Stock adjustment failed", str(error), parent=self)
