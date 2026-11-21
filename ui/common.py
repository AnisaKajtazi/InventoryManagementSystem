"""Small reusable Tkinter helpers shared by application pages."""
import tkinter as tk
from tkinter import ttk

BG = "#f3f6fb"
INK = "#172b4d"
MUTED = "#65758b"
BLUE = "#1769aa"


def page_heading(parent, title, subtitle=""):
    box = tk.Frame(parent, bg=BG)
    tk.Label(box, text=title, bg=BG, fg=INK,
             font=("Segoe UI", 14, "bold")).pack(anchor="w")
    if subtitle:
        tk.Label(box, text=subtitle, bg=BG, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 12))
    return box


def make_table(parent, columns, headings, widths=None, height=15):
    frame = ttk.Frame(parent)
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=height)
    for index, (key, label) in enumerate(zip(columns, headings)):
        tree.heading(key, text=label)
        tree.column(key, width=(widths or {}).get(key, 130), anchor="w",
                    stretch=True)
    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    tree.tag_configure("low", foreground="#b42318")
    return frame, tree


def clear_table(tree):
    tree.delete(*tree.get_children())


def card(parent, label, value, color=BLUE):
    panel = tk.Frame(parent, bg="white", highlightbackground="#e0e7f0",
                     highlightthickness=1, padx=18, pady=16)
    tk.Label(panel, text=label.upper(), bg="white", fg=MUTED,
             font=("Segoe UI", 8, "bold")).pack(anchor="w")
    value_label = tk.Label(panel, text=value, bg="white", fg=color,
                           font=("Segoe UI", 21, "bold"))
    value_label.pack(anchor="w", pady=(8, 0))
    return panel, value_label
