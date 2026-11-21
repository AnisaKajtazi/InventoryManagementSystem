"""Application entry point."""
import tkinter as tk
from tkinter import messagebox

from services.inventory import Inventory
from storage.json_storage import JSONStorage
from ui.main_window import MainWindow


def main():
    storage = JSONStorage()
    try:
        inventory = Inventory.from_dict(storage.load_data())
    except (OSError, ValueError, KeyError, TypeError) as error:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Inventory data could not be loaded",
            f"The saved inventory could not be read. Correct the JSON data and restart.\n\n{error}",
            parent=root,
        )
        root.destroy()
        return
    app = MainWindow(inventory, storage)
    app.mainloop()


if __name__ == "__main__":
    main()
