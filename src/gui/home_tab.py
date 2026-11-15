import threading
from datetime import datetime

import customtkinter as ctk

from src.gui.styles import COLORS, FONT


class HomeTab:

    def __init__(self, parent, assistant=None):
        self.tab = parent
        self.assistant = assistant
        self.root = parent.winfo_toplevel()
        self.welcome_mode = True
        self.message_labels = []
        self.create_widgets()

    # Build the welcome screen and the initially hidden chat screen
    def create_widgets(self):
        self.welcome_frame = ctk.CTkFrame(self.tab, fg_color="transparent")
        self.welcome_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.greeting_label = ctk.CTkLabel(
            self.welcome_frame,
            text="Здравствуйте",
            font=(FONT, 32, "bold"),
            text_color=COLORS["text"][0]
        )
        self.greeting_label.place(relx=0.5, rely=0.35, anchor="center")

        self.entry_welcome = ctk.CTkEntry(
            self.welcome_frame,
            font=(FONT, 14),
            placeholder_text="Спросите о чём угодно...",
            fg_color=COLORS["surface_alt"][0],
            text_color=COLORS["text"][0],
            height=50,
            corner_radius=25
        )
        self.entry_welcome.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6)
        self.entry_welcome.bind("<Return>", lambda event: self.send_message())

        chips_frame = ctk.CTkFrame(self.welcome_frame, fg_color="transparent")
        chips_frame.place(relx=0.5, rely=0.6, anchor="n")

        chip_style = {
            "font": (FONT, 12),
            "fg_color": COLORS["surface_alt"][0],
            "hover_color": COLORS["surface_alt"][1],
            "text_color": COLORS["text"][0],
            "height": 36,
            "corner_radius": 18,
            "border_width": 1,
            "border_color": COLORS["border"][0]
        }

        self.mic_button = ctk.CTkButton(
            chips_frame,
            text="Включить микрофон",
            command=self.toggle_mic,
            **chip_style
        )
        self.mic_button.pack(side="left", padx=5)

        ctk.CTkButton(
            chips_frame,
            text="Что ты умеешь?",
            command=lambda: self.send_text("Что ты умеешь?"),
            **chip_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            chips_frame,
            text="Дела",
            command=lambda: self.show_page("planner"),
            **chip_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            chips_frame,
            text="Команды",
            command=lambda: self.show_page("commands"),
            **chip_style
        ).pack(side="left", padx=5)

        self.chat_frame = ctk.CTkFrame(self.tab, fg_color="transparent")

        self.chat_scroll = ctk.CTkScrollableFrame(
            self.chat_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.chat_scroll.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        input_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.entry_chat = ctk.CTkEntry(
            input_frame,
            font=(FONT, 13),
            placeholder_text="Спросите о чём угодно...",
            fg_color=COLORS["surface_alt"][0],
            text_color=COLORS["text"][0],
            height=45
        )
        self.entry_chat.pack(fill="x", pady=(0, 10))
        self.entry_chat.bind("<Return>", lambda event: self.send_message())

        send_button = ctk.CTkButton(
            input_frame,
            text="Отправить",
            font=(FONT, 12, "bold"),
            fg_color=COLORS["accent"][0],
            hover_color=COLORS["accent"][1],
            text_color=COLORS["accent_text"][0],
            height=45,
            command=self.send_message
        )
        send_button.pack(fill="x")

    # Switch from the welcome screen to chat mode
    def switch_to_chat_mode(self):
        if not self.welcome_mode:
            return

        self.welcome_mode = False
        self.welcome_frame.place_forget()
        self.chat_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Add a message to the chat
    def add_message(self, sender, text):
        if self.welcome_mode:
            self.switch_to_chat_mode()

        msg_frame = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        msg_frame.pack(fill="x", pady=(0, 12))

        is_user = sender.lower() in ["you", "вы"]
        side = "e" if is_user else "w"
        text_color = COLORS["accent"][0] if is_user else COLORS["text"][0]

        msg_label = ctk.CTkLabel(
            msg_frame,
            text=text,
            font=(FONT, 13),
            text_color=text_color,
            wraplength=600,
            justify="left",
            anchor="w"
        )
        msg_label.pack(anchor=side, padx=10)

        timestamp = datetime.now().strftime("%H:%M")
        author = "Вы" if is_user else "Ассистент"
        footer_label = ctk.CTkLabel(
            msg_frame,
            text=f"{author} · {timestamp}",
            font=(FONT, 11),
            text_color=COLORS["muted"][0] if "muted" in COLORS else COLORS["text"][1]
        )
        footer_label.pack(anchor=side, padx=10, pady=(3, 0))

        self.message_labels.append(msg_label)

        self.chat_scroll._parent_canvas.yview_moveto(1.0)

    # Send the message from the active input; the assistant runs in a background thread
    def send_message(self):
        entry = self.entry_welcome if self.welcome_mode else self.entry_chat
        message = entry.get().strip()

        if not message:
            return

        self.add_message("You", message)
        entry.delete(0, "end")

        if self.assistant:
            threading.Thread(
                target=self._process_message_with_assistant,
                args=(message,),
                daemon=True
            ).start()
        else:
            self.process_response()

    # Fill the active input field and send immediately (used by chips)
    def send_text(self, text):
        entry = self.entry_welcome if self.welcome_mode else self.entry_chat
        entry.delete(0, "end")
        entry.insert(0, text)
        self.send_message()

    # Placeholder for the microphone button
    def toggle_mic(self):
        self.add_message("System", "Функция микрофона пока в разработке.")

    # Placeholder for navigation to other pages
    def show_page(self, page_name):
        self.add_message("System", f"Переход на страницу: {page_name}")

    # Runs in a background thread; results are posted to the UI thread via root.after
    def _process_message_with_assistant(self, message):
        try:
            response = self.assistant.process_command(message)
            self.root.after(0, lambda: self.add_message("Bot", response))
        except Exception as e:
            error_msg = f"Ошибка: {e}"
            self.root.after(0, lambda: self.add_message("Bot", error_msg))

    # Fallback reply used when no assistant is connected
    def process_response(self):
        self.add_message("Bot", "Извините, произошла ошибка при обработке сообщения.")
