"""Restock registration and searchable history."""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from ui.common import BG, make_table, clear_table


class RestockView(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(0, 14))
        self.filter = ttk.Combobox(bar, state="readonly", width=30)
        self.filter.pack(side="left")
        self.filter.bind("<<ComboboxSelected>>", lambda _e: self.refresh())
        ttk.Button(bar, text="＋ Register restock", style="Primary.TButton",
                   command=self.register).pack(side="right")
        frame, self.table = make_table(self, ("id", "product", "quantity", "timestamp"),
            ("Restock ID", "Product", "Quantity added", "Date and time"),
            {"id": 100, "product": 230, "quantity": 140, "timestamp": 220})
        frame.pack(fill="both", expand=True)

    def refresh(self):
        items = self.app.inventory.get_all_items()
        choices = ["All products"] + [f"{item.name} ({item.item_id[:8]})" for item in items]
        old = self.filter.get()
        self.filter.configure(values=choices)
        self.filter.set(old if old in choices else "All products")
        item_ids = {f"{item.name} ({item.item_id[:8]})": item.item_id for item in items}
        selected_id = item_ids.get(self.filter.get())
        clear_table(self.table)
        for record in self.app.inventory.get_restock_history():
            if selected_id and record.item_id != selected_id:
                continue
            item = self.app.inventory.get_item(record.item_id)
            self.table.insert("", "end", values=(record.restock_id[:8],
                item.name if item else "Deleted product", record.quantity_added,
                record.timestamp.replace("T", " ")))

    def register(self):
        items = self.app.inventory.get_all_items()
        if not items:
            messagebox.showinfo("No products", "Add a product before registering a restock.", parent=self)
            return
        choices = {f"{item.name} ({item.item_id[:8]})": item for item in items}
        dialog = tk.Toplevel(self)
        dialog.title("Register restock")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(padx=20, pady=18, bg="white")
        tk.Label(dialog, text="Product", bg="white").grid(row=0, column=0, sticky="w", pady=6)
        product = ttk.Combobox(dialog, state="readonly", values=list(choices), width=34)
        product.current(0)
        product.grid(row=0, column=1, pady=6)
        tk.Label(dialog, text="Quantity to add", bg="white").grid(row=1, column=0, sticky="w", pady=6)
        quantity = ttk.Entry(dialog)
        quantity.grid(row=1, column=1, pady=6)
        quantity.focus_set()

        def save():
            try:
                amount = int(quantity.get().strip())
                item = choices.get(product.get())
                if item is None:
                    raise ValueError("Select a product.")
                self.app.inventory.restock_item(item.item_id, amount)
                dialog.destroy()
                self.app.save()
                messagebox.showinfo("Restock recorded", f"Added {amount} units to {item.name}.", parent=self)
            except (ValueError, TypeError) as error:
                messagebox.showerror("Invalid restock", str(error), parent=dialog)

        buttons = ttk.Frame(dialog)
        buttons.grid(row=2, column=0, columnspan=2, sticky="e", pady=(14, 0))
        ttk.Button(buttons, text="Cancel", command=dialog.destroy).pack(side="right", padx=(8, 0))
        ttk.Button(buttons, text="Save restock", command=save).pack(side="right")
