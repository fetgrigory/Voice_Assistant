import customtkinter as ctk

COLORS = {
    "bg": ("#F7F8FA", "#17181C"),
    "surface": ("#FFFFFF", "#202126"),
    "surface_alt": ("#F0F1F4", "#292A30"),
    "border": ("#E5E6EA", "#35363D"),
    "text": ("#202127", "#F1F1F3"),
    "muted": ("#858791", "#92939D"),
    "accent": ("#DCE7FF", "#343F5B"),
    "accent_hover": ("#CAD9FA", "#414F70"),
    "accent_text": ("#315BA8", "#C5D5FF"),
    "danger": ("#FCE8E8", "#452B30"),
    "danger_hover": ("#F7D7D7", "#59363C"),
    "danger_text": ("#C64C4C", "#FF9999"),
    "success": ("#E3F5EA", "#263D31"),
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


def apply_theme():
    ctk.set_appearance_mode("System")
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


def create_button(parent, text, command, width, kind="secondary"):
    button = ctk.CTkButton(parent, text=text, command=command, width=width)
    style_button(button, kind)
    return button


# When grid_kw is provided, the title is placed via grid() instead of pack()
# so the caller can control row weights and minsizes for tight layouts.
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
        button_color=COLORS["surface_alt"],
        button_hover_color=COLORS["border"],
        text_color=COLORS["text"],
        dropdown_fg_color=COLORS["surface"],
        dropdown_text_color=COLORS["text"],
        dropdown_hover_color=COLORS["accent"],
        font=(FONT, 13),
        **kwargs
    )
