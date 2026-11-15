import customtkinter as ctk

COLORS = {
    "bg": ("#DBEAFE", "#1E293B"),
    "surface": ("#FFFFFF", "#273449"),
    "surface_alt": ("#EFF6FF", "#334155"),
    "border": ("#BFDBFE", "#475569"),
    "text": ("#1E3A5F", "#E2E8F0"),
    "muted": ("#64748B", "#94A3B8"),
    "accent": ("#3B8ED0", "#3B8ED0"),
    "accent_hover": ("#367DB5", "#2563EB"),
    "accent_text": ("#FFFFFF", "#FFFFFF"),
    "danger": ("#FEE2E2", "#3A1F25"),
    "danger_hover": ("#FECACA", "#4A2530"),
    "danger_text": ("#DC2626", "#FF657A"),
    "success": ("#16A34A", "#4BD2A0"),
    "panel": ("#FFFFFF", "#273449"),
}

FONT = "Arial"
MONO_FONT = "Consolas"

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


# Apply appearance settings
def apply_theme():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")


def style_button(button, kind="secondary"):
    button.configure(
        **BUTTON_STYLES[kind],
        corner_radius=12,
        border_width=0,
        font=(FONT, 13),
        height=38,
    )


def create_button(parent, text, command, width, kind="secondary"):
    button = ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width
    )
    style_button(button, kind)
    return button


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


def create_card(parent, **kwargs):
    return ctk.CTkFrame(
        parent,
        fg_color=COLORS["surface"],
        corner_radius=16,
        border_width=1,
        border_color=COLORS["border"],
        **kwargs
    )


def create_label(parent, text):
    return ctk.CTkLabel(
        parent,
        text=text,
        font=(FONT, 12),
        text_color=COLORS["muted"],
        anchor="w"
    )


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
        button_color=COLORS["accent"],
        button_hover_color=COLORS["accent_hover"],
        text_color=COLORS["text"],
        dropdown_fg_color=COLORS["surface"],
        dropdown_text_color=COLORS["text"],
        dropdown_hover_color=COLORS["accent"],
        font=(FONT, 13),
        **kwargs
    )
