import customtkinter as ctk

from src.gui.styles import COLORS, FONT


class HomeTab:

    def __init__(self, parent, assistant=None):
        self.tab = parent
        self.assistant = assistant

        self.create_widgets()

    def create_widgets(self):

        header_frame = ctk.CTkFrame(self.tab, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="Диалоговый чат",
            font=(FONT, 18, "bold"),
            text_color=COLORS["text"][0]
        ).pack(anchor="w")

        self.chat_frame = ctk.CTkFrame(self.tab, fg_color=COLORS["surface_alt"][0], border_width=1, border_color=COLORS["border"][0])
        self.chat_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.chat_text = ctk.CTkTextbox(
            self.chat_frame,
            font=(FONT, 13),
            fg_color=COLORS["surface_alt"][0],
            text_color=COLORS["text"][0],
            wrap="word",
            padx=15,
            pady=15,
            state="disabled"
        )
        self.chat_text.pack(fill="both", expand=True)

        input_frame = ctk.CTkFrame(self.tab, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.entry = ctk.CTkEntry(
            input_frame,
            font=(FONT, 13),
            placeholder_text="Введите сообщение...",
            fg_color=COLORS["surface_alt"][0],
            text_color=COLORS["text"][0],
            height=45
        )
        self.entry.pack(fill="x", pady=(0, 10))

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

        self.add_message("System", "Добро пожаловать! Напишите что-нибудь, чтобы начать диалог.")

    def add_message(self, sender, text):
        # The textbox must be editable to insert text
        self.chat_text.configure(state="normal")

        if sender:
            self.chat_text.insert("end", f"{sender} -> ", "bold")

        self.chat_text.insert("end", text + "\n\n", "normal")

        # Scroll to the latest message
        self.chat_text.see("end")

        # Restore read-only state
        self.chat_text.configure(state="disabled")

        self.chat_text.see("end")

    def send_message(self):
        message = self.entry.get().strip()
        if not message:
            return

        self.add_message("You", message)

        self.entry.delete(0, "end")

        # Simple keyword-based response logic
        self.process_response(message)

    def process_response(self, user_message):
        user_msg = user_message.lower()

        responses = {
            "hello": "Hi there, how can I help?",
            "hi": "Hi there, what can I do for you?",
            "hii": "Hi there, what can I do for you?",
            "hiiii": "Hi there, what can I do for you?",
            "how are you": "fine! and you?",
            "fine": "Great! how can I help you.",
            "i am good": "Great! how can I help you.",
            "i am doing good": "Great! how can I help you.",
            "thanks": "My pleasure!",
            "thank you": "My pleasure!",
            "now its my time": "My pleasure!",
            "what do you sell": "We have coffee and tea",
            "what kinds of items are there": "We have coffee and tea",
            "have you something": "We have coffee and tea",
            "tell me a joke": "What did the buffalo say when his son left for college? Bison!",
            "tell me something funny": "What did the buffalo say when his son left for college? Bison!",
            "crack a funny line": "What did the buffalo say when his son left for college? Bison!",
            "goodbye": "Have a nice day!",
            "see you later": "Have a nice day!",
            "see yaa": "Have a nice day!",
        }

        for key, response in responses.items():
            if key in user_msg:
                self.add_message("Bot", response)
                return

        # Fallback when no keyword matches
        self.add_message("Bot", "Sorry! I didn't understand that")
