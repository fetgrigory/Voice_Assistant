import customtkinter as ctk

from src.gui.sidebar import Sidebar
from src.gui.mic_tab import MicrophoneTab
from src.gui.commands_tab import CommandsTab
from src.gui.styles import COLORS, apply_theme


# Graphical interface of the voice assistant
class VoiceAssistantApp:
    def __init__(self, assistant):
        self.assistant = assistant

        self.root = ctk.CTk()
        self.root.title("Голосовой помощник")
        self.root.geometry("1200x760")
        self.root.minsize(900, 680)
        self.root.resizable(True, True)

        apply_theme()
        self.root.configure(fg_color=COLORS["bg"])

        self.create_widgets()

    # Create all UI widgets
    def create_widgets(self):
        # Main container for sidebar and content area
        main_frame = ctk.CTkFrame(self.root, fg_color=COLORS["bg"])
        main_frame.pack(fill="both", expand=True)

        # Sidebar navigation
        self.sidebar = Sidebar(
            main_frame,
            on_navigate=self.on_navigate,
            width=250,
            active="mic"
        )
        self.sidebar.pack(side="left", fill="y")

        # Content area for tabs
        self.content_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["bg"])
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Initialize tabs without displaying them yet
        self.mic_tab = MicrophoneTab(ctk.CTkFrame(self.content_frame), self.assistant)
        self.commands_tab = CommandsTab(ctk.CTkFrame(self.content_frame), self.root, self.assistant)

        # Show microphone tab by default
        self.current_tab = "mic"
        self.show_tab("mic")

    # Hide all tabs and display the selected one
    def show_tab(self, tab_name):
        self.mic_tab.tab.pack_forget()
        self.commands_tab.tab.pack_forget()

        if tab_name == "mic":
            self.mic_tab.tab.pack(fill="both", expand=True, padx=20, pady=20)
        elif tab_name == "commands":
            self.commands_tab.tab.pack(fill="both", expand=True, padx=20, pady=20)

        self.current_tab = tab_name

    # Handle sidebar navigation events
    def on_navigate(self, page):
        if page == "mic":
            self.show_tab("mic")
            self.sidebar.set_active("mic")
        elif page == "commands":
            self.show_tab("commands")
            self.sidebar.set_active("commands")
        else:
            print(f"Opened section: {page}")

    # Launch the main event loop
    def start_interface(self):
        self.root.mainloop()
