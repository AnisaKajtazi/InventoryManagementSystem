"""Main application window and page navigation."""
import tkinter as tk
from tkinter import messagebox, ttk

from ui.dashboard import DashboardView
from ui.products_view import ProductsView
from ui.categories_view import CategoriesView
from ui.stock_view import StockView
from ui.restock_view import RestockView


class MainWindow(tk.Tk):
    """Coordinate navigation, persistence, and inventory views."""

    def __init__(self, inventory, storage):
        super().__init__()
        self.inventory = inventory
        self.storage = storage
        self.title("Inventory Management System")
        self.geometry("1180x760")
        self.minsize(900, 600)
        self.configure(bg="#f3f6fb")
        self._configure_style()

        self.sidebar = tk.Frame(self, bg="#14243a", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        tk.Label(self.sidebar, text="INVENTORY\nMANAGEMENT", bg="#14243a",
                 fg="white", font=("Segoe UI", 16, "bold"), justify="left",
                 padx=22, pady=28).pack(fill="x")
        self.nav_buttons = {}
        self.content = tk.Frame(self, bg="#f3f6fb")
        self.content.pack(side="right", fill="both", expand=True)
        self.header = tk.Frame(self.content, bg="white", height=72)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        self.page_title = tk.Label(self.header, text="", bg="white", fg="#172b4d",
                                   font=("Segoe UI", 19, "bold"), padx=28)
        self.page_title.pack(side="left", fill="y")
        self.page_area = tk.Frame(self.content, bg="#f3f6fb")
        self.page_area.pack(fill="both", expand=True, padx=24, pady=22)
        self.pages = {
            "Dashboard": DashboardView,
            "Products": ProductsView,
            "Categories": CategoriesView,
            "Stock Management": StockView,
            "Restock History": RestockView,
        }
        for name in self.pages:
            button = tk.Button(self.sidebar, text=name, anchor="w", relief="flat",
                               bd=0, padx=24, pady=13, bg="#14243a", fg="#d7e0ec",
                               activebackground="#24466c", activeforeground="white",
                               font=("Segoe UI", 10, "bold"), cursor="hand2",
                               command=lambda page=name: self.show_page(page))
            button.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[name] = button
        self.protocol("WM_DELETE_WINDOW", self._close)
        self.show_page("Dashboard")

    def _configure_style(self):
        style = ttk.Style(self)
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 9),
                        background="white", fieldbackground="white")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"),
                        background="#eaf0f8", foreground="#243b5a")
        style.configure("Primary.TButton", font=("Segoe UI", 9, "bold"),
                        padding=(12, 8))

    def refresh_all(self):
        """Refresh visible and cached views after a successful change."""
        for child in self.page_area.winfo_children():
            if hasattr(child, "refresh"):
                child.refresh()

    def show_page(self, name):
        self.page_title.configure(text=name)
        for nav_name, button in self.nav_buttons.items():
            button.configure(bg="#24466c" if nav_name == name else "#14243a",
                             fg="white" if nav_name == name else "#d7e0ec")
        for child in self.page_area.winfo_children():
            child.destroy()
        view = self.pages[name](self.page_area, self)
        view.pack(fill="both", expand=True)
        view.refresh()

    def save(self):
        """Persist the current inventory and refresh all derived views."""
        try:
            self.storage.save_data(self.inventory)
        except (OSError, ValueError, TypeError) as error:
            messagebox.showerror("Save failed", f"Could not save inventory:\n{error}", parent=self)
            raise
        self.refresh_all()

    def _close(self):
        try:
            self.storage.save_data(self.inventory)
        except OSError as error:
            if not messagebox.askyesno("Save failed", f"Could not save:\n{error}\nClose anyway?", parent=self):
                return
        self.destroy()
