import customtkinter as ctk


COLORS = {
    "bg": ("#151923", "#151923"),
    "surface": ("#1c2230", "#1c2230"),
    "surface_alt": ("#252d3d", "#252d3d"),
    "border": ("#303b53", "#303b53"),
    "text": ("#e8ecf5", "#e8ecf5"),
    "muted": ("#8f9bb0", "#8f9bb0"),
    "accent": ("#8b7bff", "#8b7bff"),
    "accent_hover": ("#a090ff", "#a090ff"),
    "accent_text": ("#ffffff", "#ffffff"),
    "danger": ("#3a1f25", "#3a1f25"),
    "danger_hover": ("#4a2530", "#4a2530"),
    "danger_text": ("#ff657a", "#ff657a"),
    "success": ("#4bd2a0", "#4bd2a0"),
}

FONT = "Arial"
MONO_FONT = "Consolas"

# Button style presets
BUTTON_STYLES = {
    "primary": {
        "fg_color": COLORS["accent"],
        "hover_color": COLORS["accent_hover"],
        "text_color": COLORS["accent_text"],
    },
    "secondary": {
        "fg_color": COLORS["surface_alt"],
        "hover_color": COLORS["border"],
        "text_color": COLORS["text"],
    },
    "danger": {
        "fg_color": COLORS["danger"],
        "hover_color": COLORS["danger_hover"],
        "text_color": COLORS["danger_text"],
    },
}


# Apply the dark theme globally
def apply_theme():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")


# Apply Astra-inspired button styling
def style_button(button, kind="secondary"):
    button.configure(
        **BUTTON_STYLES[kind],
        corner_radius=12,
        border_width=0,
        font=(FONT, 13),
        height=38,
    )


# Create a styled button with the given parameters
def create_button(parent, text, command, width, kind="secondary"):
    button = ctk.CTkButton(parent, text=text, command=command, width=width)
    style_button(button, kind)
    return button


# Create a section title with optional description
def create_section_title(parent, title, description=None, grid_kw=None):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    if grid_kw is not None:
        frame.grid(**grid_kw)
    else:
        frame.pack(fill="x", padx=20, pady=(10, 6))

    ctk.CTkLabel(
        frame,
        text=title,
        font=(FONT, 21, "bold"),
        text_color=COLORS["text"],
        anchor="w"
    ).pack(anchor="w")

    if description:
        ctk.CTkLabel(
            frame,
            text=description,
            font=(FONT, 12),
            text_color=COLORS["muted"],
            anchor="w"
        ).pack(anchor="w", pady=(4, 0))

    return frame


# Create a card frame with border
def create_card(parent, **kwargs):
    return ctk.CTkFrame(
        parent,
        fg_color=COLORS["surface"],
        corner_radius=16,
        border_width=1,
        border_color=COLORS["border"],
        **kwargs
    )


# Create a muted label
def create_label(parent, text):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=(FONT, 12),
        text_color=COLORS["muted"],
        anchor="w"
    )


# Create a text entry field
def create_entry(parent, placeholder="", width=300):
    return ctk.CTkEntry(
        parent,
        width=width,
        height=40,
        placeholder_text=placeholder,
        corner_radius=10,
        border_width=1,
        border_color=COLORS["border"],
        fg_color=COLORS["surface_alt"],
        text_color=COLORS["text"],
        placeholder_text_color=COLORS["muted"],
        font=(FONT, 13)
    )


# Create a dropdown combobox
def create_combobox(parent, values, width, height, **kwargs):
    return ctk.CTkComboBox(
        parent,
        values=values,
        width=width,
        height=height,
        corner_radius=10,
        border_width=1,
        border_color=COLORS["border"],
        fg_color=COLORS["surface_alt"],
        button_color=COLORS["surface_alt"],
        button_hover_color=COLORS["border"],
        text_color=COLORS["text"],
        dropdown_fg_color=COLORS["surface"],
        dropdown_text_color=COLORS["text"],
        dropdown_hover_color=COLORS["accent"],
        font=(FONT, 13),
        **kwargs
    )