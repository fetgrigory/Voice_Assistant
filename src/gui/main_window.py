import customtkinter as ctk

from src.gui.commands_tab import CommandsTab
from src.gui.mic_tab import MicrophoneTab
from src.gui.styles import COLORS, FONT, apply_theme


# Graphical interface of the voice assistant
class VoiceAssistantApp:
    def __init__(self, assistant):
        self.assistant = assistant

        self.root = ctk.CTk()
        self.root.title("Голосовой помощник")
        self.root.geometry("1000x760")
        self.root.minsize(900, 680)
        self.root.resizable(True, True)

        apply_theme()
        self.root.configure(fg_color=COLORS["bg"])

        self.create_widgets()

# The mic tab goes first: it connects the log handler before the commands tab starts logging
    def create_widgets(self):
        header = ctk.CTkFrame(self.root, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 5))

        ctk.CTkLabel(
            header,
            text="Голосовой помощник",
            font=(FONT, 25, "bold"),
            text_color=COLORS["text"]
        ).pack(side="left")

        self.notebook = ctk.CTkTabview(
            self.root,
            fg_color=COLORS["bg"],
            segmented_button_fg_color=COLORS["surface_alt"],
            segmented_button_selected_color=COLORS["accent"],
            segmented_button_selected_hover_color=COLORS["accent_hover"],
            segmented_button_unselected_color=COLORS["surface_alt"],
            segmented_button_unselected_hover_color=COLORS["border"],
            text_color=COLORS["text"],
            corner_radius=14,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.notebook.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        self.mic_tab = MicrophoneTab(self.notebook.add("Микрофон"), self.assistant)
        self.commands_tab = CommandsTab(self.notebook.add("Команды"), self.root, self.assistant)

    def start_interface(self):
        self.root.mainloop()
