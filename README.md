# Inventory Management System

A desktop inventory application for the **Advanced Programming** course. It manages product and category records, stock levels, replenishment history, low stock alerts, and inventory value. Data is stored locally in JSON.

## Features

- Product create, edit, delete, search, and category/stock filtering
- Category management with duplicate-name and in-use deletion checks
- Stock adjustments with per-product low-stock thresholds
- Restock transactions that update stock and preserve a timestamped history
- Dashboard with live inventory statistics, low stock items, and recent restocks
- Automatic persistence after successful changes

## Technologies

- Python 3.10 or later
- Tkinter and `ttk` for the desktop interface
- JSON for local storage
- Python standard library only; no third-party packages are required

## Project structure

```text
main.py                 Application startup and dependency wiring
models/                 Item, Category, and Restock entities
services/inventory.py   Inventory business rules
storage/                JSON persistence and inventory.json
ui/                     Window, dashboard, and management views
ui/dialogs/             Product and category forms
utils/                  Shared validation/constants
```

## Installation and launch

From the project root, optionally activate the existing virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

No package installation is needed. Launch the application with:

```powershell
python main.py
```

Tkinter must be available in your Python installation. The application creates `storage/inventory.json` with an empty inventory on first launch; existing saved data is loaded automatically.

## Basic usage

1. Open **Categories** and create at least one category.
2. Add products in **Products** and assign each to a category.
3. Use **Stock Management** to add or remove stock. A removal cannot exceed the available quantity.
4. Record supplier replenishments in **Restock History**. These records also increase product stock.
5. Review totals and alerts on **Dashboard**. Changes are written to JSON immediately.

Products with replenishment history cannot be deleted, which keeps historical records linked to a valid product. Categories that still contain products cannot be deleted.
