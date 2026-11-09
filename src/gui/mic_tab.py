import logging
import tkinter as tk
from contextlib import suppress
from tkinter import messagebox

import customtkinter as ctk
import sounddevice as sd

from .styles import (COLORS, FONT, MONO_FONT, create_button, create_card,
                     create_combobox, create_section_title)


# Custom logging handler that writes messages into a CTkTextbox
class TkinterLogHandler(logging.Handler):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox

    # Logs may come from other threads, so the update is scheduled in the Tk main loop
    def emit(self, record):
        msg = self.format(record)

        def append():
            with suppress(tk.TclError):
                self.textbox.configure(state="normal")
                self.textbox.insert("end", msg + "\n")
                self.textbox.see("end")
                self.textbox.configure(state="disabled")

        with suppress(tk.TclError):
            self.textbox.after(0, append)


# "Микрофон" tab: input device, assistant name (also the activation word) and event log
class MicrophoneTab:
    def __init__(self, parent, assistant):
        self.tab = parent
        self.assistant = assistant
        self.device_combobox = None
        self.assistant_name_var = None
        self.assistant_name_entry = None
        self.log_textbox = None

        self.create_widgets()
        self.setup_logging()

    # Grid reserves stable height for the logs card; propagation is off so it never collapses
    def create_widgets(self):
        self.tab.grid_columnconfigure(0, weight=1)
        self.tab.grid_rowconfigure(0, weight=0)
        self.tab.grid_rowconfigure(1, weight=0)
        self.tab.grid_rowconfigure(2, weight=0)
        self.tab.grid_rowconfigure(3, weight=1, minsize=240)

        create_section_title(
            self.tab,
            "Настройки микрофона",
            "Управление устройством голосового ввода",
            grid_kw={"row": 0, "column": 0, "sticky": "ew", "padx": 20, "pady": (10, 6)}
        )

        settings_frame = create_card(self.tab)
        settings_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=6)

        content = ctk.CTkFrame(settings_frame, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=12)

        self.create_device_section(content)
        self.create_name_section(content)

        save_button = create_button(content, "Сохранить изменения", self.save_changes, 190, "primary")
        save_button.pack(anchor="w", pady=(18, 0))

        create_section_title(
            self.tab,
            "Журнал событий",
            "Последние действия и сообщения голосового помощника",
            grid_kw={"row": 2, "column": 0, "sticky": "ew", "padx": 20, "pady": (10, 6)}
        )

        logs_frame = create_card(self.tab)
        logs_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(6, 14))
        logs_frame.pack_propagate(False)
        logs_frame.grid_propagate(False)

        self.log_textbox = ctk.CTkTextbox(
            logs_frame,
            wrap="word",
            height=200,
            corner_radius=12,
            border_width=0,
            fg_color="transparent",
            text_color=COLORS["text"],
            font=(MONO_FONT, 11),
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["muted"]
        )
        self.log_textbox.pack(fill="both", expand=True, padx=12, pady=12)
        self.log_textbox.configure(state="disabled")

    def create_device_section(self, content):
        ctk.CTkLabel(
            content,
            text="Входное устройство",
            font=(FONT, 15, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            content,
            text="Выберите микрофон, который будет использовать ассистент.",
            font=(FONT, 12),
            text_color=COLORS["muted"]
        ).pack(anchor="w", pady=(5, 14))

        saved_device = self.get_device_by_index(self.assistant.input_device)
        self.device_combobox = create_combobox(content, self.get_input_devices(), width=400, height=42)
        self.device_combobox.set(saved_device if saved_device else self.get_default_input_device())
        self.device_combobox.pack(anchor="w")

    def create_name_section(self, content):
        ctk.CTkLabel(
            content,
            text="Имя ассистента",
            font=(FONT, 15, "bold"),
            text_color=COLORS["text"]
        ).pack(anchor="w", pady=(22, 0))

        ctk.CTkLabel(
            content,
            text="Это имя также служит активационным словом. Вводите его так, как оно распознаётся речью.",
            font=(FONT, 12),
            text_color=COLORS["muted"]
        ).pack(anchor="w", pady=(5, 14))

        self.assistant_name_var = ctk.StringVar(value=self.assistant.assistant_name)

        self.assistant_name_entry = ctk.CTkEntry(
            content,
            textvariable=self.assistant_name_var,
            font=(FONT, 14, "bold"),
            text_color=COLORS["text"],
            fg_color=COLORS["surface_alt"],
            border_color=COLORS["border"],
            width=200,
            height=35
        )
        self.assistant_name_entry.pack(anchor="w")

    def setup_logging(self):
        log_handler = TkinterLogHandler(self.log_textbox)
        log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        root_logger = logging.getLogger()
        root_logger.addHandler(log_handler)
        root_logger.setLevel(logging.INFO)

    def get_device_by_index(self, index):
        devices = sd.query_devices()
        if 0 <= index < len(devices):
            return f"{index}: {devices[index]['name']}"
        return None

    def get_input_devices(self):
        devices = sd.query_devices()
        input_devices = []
        for i, device in enumerate(devices):
            if device["max_input_channels"] > 0:
                input_devices.append(f"{i}: {device['name']}")
        return input_devices if input_devices else ["Нет доступных устройств ввода"]

    def get_default_input_device(self):
        default_input_device = sd.default.device[0]
        devices = sd.query_devices()
        if 0 <= default_input_device < len(devices):
            return f"{default_input_device}: {devices[default_input_device]['name']}"
        return "Выберите устройство ввода"

    # Single handler for the shared save button: applies both the device and the name
    def save_changes(self):
        self.save_device()
        self.save_assistant_name()

    # Saves the selected device and updates it in Assistant
    def save_device(self):
        selected = self.device_combobox.get()
        # Real devices look like "3: Name"; placeholder texts have no index
        try:
            device_index = int(selected.split(":")[0])
        except ValueError:
            logging.info("Устройство не выбрано.")
            return

        try:
            self.assistant.set_input_device(device_index)
            logging.info("Выбрано устройство: %s", selected)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить устройство: {e}")

    # Updates the name and the activation word in Assistant
    def save_assistant_name(self):
        try:
            self.assistant.set_assistant_name(self.assistant_name_var.get())
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить имя: {e}")