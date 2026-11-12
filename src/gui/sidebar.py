import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from src.gui.styles import COLORS, FONT


class Sidebar(tk.Frame):

    # Menu structure: only essential sections
    GROUPS = [
        ("Главное", [
            ("Главная", "home_tab"),
        ]),
        ("Основное", [
            ("Микрофон", "mic"),
            ("Команды", "commands"),
        ]),
    ]

    def __init__(
        self,
        master,
        on_navigate: Optional[Callable[[str], None]] = None,
        width=250,
        active="home_tab",
        hidden_items=None,
        **kwargs
    ):
        super().__init__(
            master,
            bg=COLORS["bg"][0],
            width=width,
            **kwargs
        )

        self.pack_propagate(False)

        self.on_navigate = on_navigate
        self.active = active

        self.buttons = {}
        self.badges = {}

        self.hidden_items = set(hidden_items or [])

        self.build_header()
        self.build_menu()

        self.set_active(active)

    # Build header with subtitle only
    def build_header(self):
        header = tk.Frame(self, bg=COLORS["bg"][0], padx=17, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="голосовой ассистент",
            bg=COLORS["bg"][0],
            fg=COLORS["muted"][0],
            font=(FONT, 11),
            anchor="w"
        ).pack(anchor="w")

    # Build scrollable menu container
    def build_menu(self):
        container = tk.Frame(self, bg=COLORS["bg"][0])
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg=COLORS["bg"][0], highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.menu = tk.Frame(self.canvas, bg=COLORS["bg"][0])
        self.menu_window = self.canvas.create_window((0, 0), window=self.menu, anchor="nw")

        self.menu.bind("<Configure>", self.update_scroll)
        self.canvas.bind("<Configure>", self.resize_menu)
        self.canvas.bind_all("<MouseWheel>", self.mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        # Build menu groups and items
        for group, items in self.GROUPS:
            if group:
                tk.Label(
                    self.menu,
                    text=group.upper(),
                    bg=COLORS["bg"][0],
                    fg=COLORS["muted"][0],
                    font=(FONT, 8, "bold"),
                    anchor="w",
                    padx=17,
                    pady=9
                ).pack(fill="x")

            for label, key in items:
                if key in self.hidden_items:
                    continue
                self.add_item(label, key)

        self.update_scroll()

    # Add a single menu item with badge
    def add_item(self, label, key):
        row = tk.Frame(self.menu, bg=COLORS["bg"][0])
        row.pack(fill="x", padx=8, pady=1)

        button = self.make_button(row, label, lambda k=key: self.navigate(k))
        button.pack(side="left", fill="x", expand=True)

        badge = tk.Label(
            row,
            text="",
            bg=COLORS["bg"][0],
            fg=COLORS["danger_text"][0],
            font=(FONT, 13, "bold")
        )
        badge.pack(side="right", padx=10)

        self.buttons[key] = button
        self.badges[key] = badge

        button.bind("<Enter>", lambda e, k=key: self.hover(k, True))
        button.bind("<Leave>", lambda e, k=key: self.hover(k, False))

    # Create a flat styled button
    def make_button(self, parent, text, command, accent=False):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=COLORS["panel"][0] if accent else COLORS["bg"][0],
            fg=COLORS["accent"][0] if accent else COLORS["text"][0],
            activebackground=COLORS["surface_alt"][0],
            activeforeground=COLORS["text"][0],
            relief="flat",
            bd=0,
            anchor="w",
            padx=11,
            pady=8,
            cursor="hand2",
            font=(FONT, 9),
            highlightthickness=0
        )

    # Handle navigation and notify listener
    def navigate(self, key):
        self.set_active(key)
        if self.on_navigate:
            self.on_navigate(key)

    # Highlight the active menu item
    def set_active(self, key):
        self.active = key
        for item_key, button in self.buttons.items():
            selected = item_key == key
            button.configure(
                bg=COLORS["accent"][0] if selected else COLORS["bg"][0],
                fg=COLORS["accent_text"][0] if selected else COLORS["text"][0],
                font=(FONT, 9, "bold" if selected else "normal")
            )

    # Handle hover state for menu items
    def hover(self, key, entered):
        if key == self.active:
            return
        button = self.buttons.get(key)
        if button:
            button.configure(bg=COLORS["surface_alt"][0] if entered else COLORS["bg"][0])

    # Toggle badge indicator for an item
    def set_badge(self, key, enabled=True):
        badge = self.badges.get(key)
        if badge:
            badge.configure(text="●" if enabled else "")

    # Add a new menu item dynamically
    def add_plugin(self, label, key):
        if key in self.buttons:
            return
        self.add_item(label, key)
        self.menu.update_idletasks()
        self.update_scroll()

    # Remove a menu item by key
    def remove_item(self, key):
        button = self.buttons.pop(key, None)
        self.badges.pop(key, None)
        if button:
            button.master.destroy()

    # Update scroll region after content changes
    def update_scroll(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Resize menu frame to match canvas width
    def resize_menu(self, event):
        self.canvas.itemconfigure(self.menu_window, width=event.width)

    # Handle mouse wheel scrolling
    def mousewheel(self, event):
        x, y = self.winfo_pointerxy()
        widget = self.winfo_containing(x, y)
        if widget and str(widget).startswith(str(self)):
            self.canvas.yview_scroll(int(-event.delta / 120), "units")
