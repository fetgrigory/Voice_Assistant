import json
import logging
import os
import inspect
import tkinter as tk
import customtkinter as ctk
import sounddevice as sd
from tkinter import messagebox
# Theme configuration and styling helpers
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
# Apply Astra-inspired button styling
def style_button(button, kind="secondary"):
    styles = {
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
    button.configure(
        **styles[kind],
        corner_radius=12,
        border_width=0,
        font=(FONT, 13),
        height=38,
    )
# Custom logging handler that writes messages into a CTkTextbox
class TkinterLogHandler(logging.Handler):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox
    # Inserts formatted log records into the textbox safely via Tkinter event loop
    def emit(self, record):
        msg = self.format(record)
        def append():
            try:
                self.textbox.configure(state="normal")
                self.textbox.insert("end", msg + "\n")
                self.textbox.see("end")
                self.textbox.configure(state="disabled")
            except tk.TclError:
                pass
        # Schedule GUI update in the main thread
        try:
            self.textbox.after(0, append)
        except tk.TclError:
            pass
# Graphical interface of the voice assistant
class VoiceAssistantApp:
    COMMANDS_FILE = "src/config/commands.json"
    VALID_HANDLERS = [
        "self",
        "system_control",
        "network_actions",
    ]
    def __init__(self, assistant):
        self.assistant = assistant
        # Initialize main window
        self.root = ctk.CTk()
        self.root.title("Голосовой помощник")
        self.root.geometry("1000x760")
        self.root.minsize(900, 680)
        self.root.resizable(True, True)
        # Configure appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.root.configure(fg_color=COLORS["bg"])
        # Selected audio input device
        self.selected_device = None
        # Initialize command tracking variables
        self.selected_command_name = None
        self.commands_data = []
        # Initialize UI components
        self.notebook = None
        self.mic_tab = None
        self.commands_tab = None
        self.commands_frame = None
        self.commands_list_textbox = None
        self.commands_buttons_frame = None
        self.add_command_button = None
        self.edit_command_button = None
        self.delete_command_button = None
        self.mic_frame = None
        self.logs_frame = None
        self.log_textbox = None
        self.device_combobox = None
        self.save_button = None
        self.log_handler = None
        # Create main interface elements
        self.create_widgets()
        # Load and display commands
        self.load_commands()
        # Configure textbox for log output
        self.log_textbox.configure(state="disabled")
    # Helper to create section titles
    # When grid_kw is provided, the title is placed via grid() instead of pack()
    # so the caller can control row weights and minsizes for tight layouts.
    def create_section_title(self, parent, title, description=None, grid_kw=None):
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
    # Helper to create styled cards
    def create_card(self, parent, **kwargs):
        return ctk.CTkFrame(
            parent,
            fg_color=COLORS["surface"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["border"],
            **kwargs
        )
    # Helper to create labels
    def create_label(self, parent, text):
        return ctk.CTkLabel(
            parent,
            text=text,
            font=(FONT, 12),
            text_color=COLORS["muted"],
            anchor="w"
        )
    # Helper to create entry fields
    def create_entry(self, parent, placeholder="", width=300):
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
    # Helper to create dialog buttons
    def create_dialog_button(self, parent, text, command, kind="secondary"):
        button = ctk.CTkButton(parent, text=text, command=command, width=130)
        style_button(button, kind)
        return button
    # Build the main user interface
    def create_widgets(self):
        # Create header
        header = ctk.CTkFrame(self.root, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(20, 5))
        ctk.CTkLabel(
            header,
            text="Голосовой помощник",
            font=(FONT, 25, "bold"),
            text_color=COLORS["text"]
        ).pack(side="left")
        ctk.CTkLabel(
            header,
            text="ASTRA",
            font=(FONT, 11, "bold"),
            text_color=COLORS["muted"]
        ).pack(side="right", padx=5)
        # Create notebook for tabs
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
        self.mic_tab = self.notebook.add("Микрофон")
        self.commands_tab = self.notebook.add("Команды")
        self.create_microphone_tab()
        self.create_commands_tab()
        # Connect logging system to textbox
        self.log_handler = TkinterLogHandler(self.log_textbox)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        self.log_handler.setFormatter(formatter)
        
        root_logger = logging.getLogger()
        root_logger.addHandler(self.log_handler)
        root_logger.setLevel(logging.INFO)
    # Add microphone controls to the mic tab
    def create_microphone_tab(self):
        # Use grid for the mic tab so the logs panel is guaranteed a stable
        # slice of vertical space. With the old pack()+expand=True setup, the
        # logs card was squeezed to ~42px (textbox only ~18px) because the mic
        # settings card already consumed the available height, which made log
        # messages technically inserted but invisible to the user.
        self.mic_tab.grid_columnconfigure(0, weight=1)
        self.mic_tab.grid_rowconfigure(0, weight=0)  # section title
        self.mic_tab.grid_rowconfigure(1, weight=0)  # mic settings card
        self.mic_tab.grid_rowconfigure(2, weight=0)  # section title
        self.mic_tab.grid_rowconfigure(3, weight=1, minsize=240)  # logs card

        self.create_section_title(
            self.mic_tab,
            "Настройки микрофона",
            "Управление устройством голосового ввода",
            grid_kw={"row": 0, "column": 0, "sticky": "ew", "padx": 20, "pady": (10, 6)}
        )
        # Frame for microphone selection
        self.mic_frame = self.create_card(self.mic_tab)
        self.mic_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=6)
        content = ctk.CTkFrame(self.mic_frame, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=12)
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
        self.device_options = self.get_input_devices()
        saved_device = self.get_device_by_index(self.assistant.input_device)
        self.device_combobox = ctk.CTkComboBox(
            content,
            values=self.device_options,
            width=400,
            height=42,
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
            font=(FONT, 13)
        )
        self.device_combobox.set(saved_device if saved_device else self.get_default_input_device())
        self.device_combobox.pack(anchor="w")
        self.save_button = ctk.CTkButton(content, text="Сохранить изменения", command=self.save_device, width=190)
        style_button(self.save_button, "primary")
        self.save_button.pack(anchor="w", pady=(18, 0))
        # Logs List (for displaying assistant logs)
        self.create_section_title(
            self.mic_tab,
            "Журнал событий",
            "Последние действия и сообщения голосового помощника",
            grid_kw={"row": 2, "column": 0, "sticky": "ew", "padx": 20, "pady": (10, 6)}
        )
        self.logs_frame = self.create_card(self.mic_tab)
        self.logs_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=(6, 14))
        # Prevent the card from collapsing below the textbox's natural size,
        # so the log area is never squeezed to nothing again.
        self.logs_frame.pack_propagate(False)
        self.logs_frame.grid_propagate(False)
        # Logs textbox
        self.log_textbox = ctk.CTkTextbox(
            self.logs_frame,
            wrap="word",
            height=200,
            corner_radius=12,
            border_width=0,
            fg_color="transparent",
            text_color=COLORS["text"],
            font=("Consolas", 11),
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["muted"]
        )
        self.log_textbox.pack(fill="both", expand=True, padx=12, pady=12)
    # Create commands management tab
    def create_commands_tab(self):
        self.create_section_title(
            self.commands_tab,
            "Управление командами",
            "Создавайте, редактируйте и удаляйте голосовые команды"
        )
        # Frame for commands list
        self.commands_frame = self.create_card(self.commands_tab)
        self.commands_frame.pack(fill="both", expand=True, padx=20, pady=(5, 10))
        self.commands_list_textbox = ctk.CTkTextbox(
            self.commands_frame,
            wrap="word",
            corner_radius=12,
            border_width=0,
            fg_color="transparent",
            text_color=COLORS["text"],
            font=(FONT, 13),
            scrollbar_button_color=COLORS["border"],
            scrollbar_button_hover_color=COLORS["muted"]
        )
        self.commands_list_textbox.pack(fill="both", expand=True, padx=12, pady=12)
        # Bind command selection event
        self.commands_list_textbox._textbox.bind("<Button-1>", self._on_command_click, add="+")
        self.commands_list_textbox._textbox.tag_configure("selected", background=COLORS["accent"][0])
        # Frame for buttons
        self.commands_buttons_frame = ctk.CTkFrame(self.commands_tab, fg_color="transparent")
        self.commands_buttons_frame.pack(fill="x", padx=20, pady=(5, 15))
        # Add command button
        self.add_command_button = ctk.CTkButton(
            self.commands_buttons_frame,
            text="+  Добавить команду",
            command=self.open_add_command_window,
            width=175
        )
        style_button(self.add_command_button, "primary")
        self.add_command_button.pack(side="left", padx=(0, 8))
        # Edit command button
        self.edit_command_button = ctk.CTkButton(
            self.commands_buttons_frame,
            text="Редактировать",
            command=self.edit_command,
            width=145
        )
        style_button(self.edit_command_button, "secondary")
        self.edit_command_button.pack(side="left", padx=8)
        # Delete command button
        self.delete_command_button = ctk.CTkButton(
            self.commands_buttons_frame,
            text="Удалить",
            command=self.delete_command,
            width=110
        )
        style_button(self.delete_command_button, "danger")
        self.delete_command_button.pack(side="left", padx=8)
    # Handle command selection click
    def _on_command_click(self, event):
        widget = event.widget
        try:
            index = widget.index(f"@{event.x},{event.y}")
            line_number = int(index.split(".")[0])
            line_start = widget.index(f"{line_number}.0")
            line_end = widget.index(f"{line_number}.end")
            clicked_line = widget.get(line_start, line_end)
            # Parse command name from selection
            command_name = None
            for line in range(line_number, 0, -1):
                content = widget.get(f"{line}.0", f"{line}.end")
                if content.startswith("Команда: "):
                    command_name = content.replace("Команда: ", "", 1).strip()
                    break
            if command_name and any(cmd.get("command") == command_name for cmd in self.commands_data):
                self.selected_command_name = command_name
                # Highlight selected command block
                widget.tag_remove("selected", "1.0", "end")
                start_line = line_number
                while start_line > 1:
                    previous = widget.get(f"{start_line - 1}.0", f"{start_line - 1}.end")
                    if previous.startswith("Команда: "):
                        break
                    start_line -= 1
                end_line = start_line + 1
                while end_line <= int(widget.index("end-1c").split(".")[0]):
                    current = widget.get(f"{end_line}.0", f"{end_line}.end")
                    if current.startswith("Команда: ") and end_line != start_line:
                        break
                    end_line += 1
                widget.tag_add("selected", f"{start_line}.0", f"{end_line}.0")
        except (tk.TclError, ValueError):
            pass
    # Load commands from JSON and display them
    def load_commands(self):
        try:
            if os.path.exists(self.COMMANDS_FILE):
                with open(self.COMMANDS_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                self.commands_data = data.get("commands", [])
            else:
                self.commands_data = []
            self.display_commands(self.commands_data)
        except Exception as e:
            logging.error("Ошибка загрузки команд: %s", e)
            self.commands_data = []
            self.display_commands([])
    # Display commands in the textbox
    def display_commands(self, commands):
        textbox = self.commands_list_textbox
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        self.selected_command_name = None
        if not commands:
            textbox.insert("end", "\n\n          Команды пока не добавлены.\n          Нажмите «Добавить команду», чтобы создать первую.")
        for index, cmd in enumerate(commands):
            triggers = ", ".join(cmd.get("triggers", []))
            parameters = ", ".join(cmd.get("parameters", []))
            say = cmd.get("say", "")
            command_text = (
                f"Команда: {cmd.get('command', '')}\n"
                f"Триггеры: {triggers}\n"
                f"Действие: {cmd.get('make', '')}\n"
                f"Обработчик: {cmd.get('handler', '')}\n"
                f"Параметры: {parameters}\n"
                f"Ответ: {say}\n"
                f"{'─' * 55}\n\n"
            )
            textbox.insert("end", command_text)
        textbox.configure(state="disabled")
    # Create base dialog window for commands
    def create_command_dialog(self, title):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("480x650")
        dialog.resizable(False, False)
        dialog.configure(fg_color=COLORS["bg"])
        dialog.transient(self.root)
        dialog.grab_set()
        header = ctk.CTkFrame(dialog, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(22, 10))
        ctk.CTkLabel(header, text=title, font=(FONT, 21, "bold"), text_color=COLORS["text"]).pack(anchor="w")
        ctk.CTkLabel(header, text="Настройте параметры голосовой команды", font=(FONT, 12), text_color=COLORS["muted"]).pack(anchor="w", pady=(5, 0))
        card = self.create_card(dialog)
        card.pack(fill="both", expand=True, padx=20, pady=10)
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)
        return dialog, content
    # Helper to create dialog input fields
    def create_dialog_field(self, parent, label, placeholder="", value=None):
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=6)
        self.create_label(field_frame, label).pack(anchor="w", pady=(0, 5))
        entry = self.create_entry(field_frame, placeholder=placeholder, width=400)
        if value is not None:
            entry.insert(0, str(value))
        entry.pack(fill="x")
        return entry
    # Helper to create handler combobox
    def create_handler_field(self, parent, value="self"):
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=6)
        self.create_label(field_frame, "Обработчик:").pack(anchor="w", pady=(0, 5))
        handler_var = ctk.StringVar(value=value)
        combobox = ctk.CTkComboBox(
            field_frame,
            values=self.VALID_HANDLERS,
            variable=handler_var,
            width=400,
            height=40,
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
            font=(FONT, 13)
        )
        combobox.pack(fill="x")
        return handler_var
    # Helper to create dialog buttons
    def create_dialog_buttons(self, parent, save_command, dialog):
        buttons = ctk.CTkFrame(parent, fg_color="transparent")
        buttons.pack(fill="x", pady=(15, 5))
        cancel_button = self.create_dialog_button(buttons, "Отмена", dialog.destroy, "secondary")
        cancel_button.pack(side="right", padx=(8, 0))
        save_button = self.create_dialog_button(buttons, "Сохранить", save_command, "primary")
        save_button.pack(side="right")
    # Open window for adding new command
    def open_add_command_window(self):
        dialog, content = self.create_command_dialog("Добавление команды")
        command_entry = self.create_dialog_field(content, "Название команды:", "Например: открыть браузер")
        triggers_entry = self.create_dialog_field(content, "Триггеры (через запятую):", "Например: браузер, открой браузер")
        make_entry = self.create_dialog_field(content, "Действие:", "Название метода")
        handler_var = self.create_handler_field(content)
        parameters_entry = self.create_dialog_field(content, "Параметры (через запятую):", "Параметры метода")
        say_entry = self.create_dialog_field(content, "Голосовой ответ:", "Ответ ассистента")
        def save_command():
            try:
                command_name = command_entry.get().strip()
                triggers = [t.strip() for t in triggers_entry.get().split(",") if t.strip()]
                make_action = make_entry.get().strip()
                handler = handler_var.get()
                parameters = [p.strip() for p in parameters_entry.get().split(",") if p.strip()]
                say = say_entry.get().strip()
                if not command_name or not triggers or not make_action:
                    messagebox.showerror("Ошибка", "Заполните обязательные поля: название, триггеры, действие", parent=dialog)
                    return
                # Validate command
                if not self.validate_command(command_name, make_action, handler, parameters):
                    return
                # Add command to JSON
                self.add_command_to_json({
                    "command": command_name,
                    "make": make_action,
                    "handler": handler,
                    "parameters": parameters,
                    "say": say,
                    "triggers": triggers
                })
                # Update display
                self.load_commands()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения команды: {e}", parent=dialog)
        self.create_dialog_buttons(content, save_command, dialog)
    # Validate command parameters
    def validate_command(self, command_name, make_action, handler, parameters, exclude_command=None):
        # Check if command name is unique
        if os.path.exists(self.COMMANDS_FILE):
            try:
                with open(self.COMMANDS_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                for cmd in data.get("commands", []):
                    if cmd.get("command") == command_name and cmd.get("command") != exclude_command:
                        messagebox.showerror("Ошибка", f"Команда с именем '{command_name}' уже существует")
                        return False
            except Exception:
                pass
        # Validate handler
        if handler not in self.VALID_HANDLERS:
            messagebox.showerror("Ошибка", f"Некорректный обработчик. Допустимые: {', '.join(self.VALID_HANDLERS)}")
            return False
        # Validate method exists
        try:
            target = None
            if handler == "self":
                target = self.assistant
            elif handler == "system_control":
                target = self.assistant.system_control
            elif handler == "network_actions":
                target = self.assistant.network_actions
            if target is None or not hasattr(target, make_action):
                messagebox.showerror("Ошибка", f"Метод '{make_action}' не существует в обработчике '{handler}'")
                return False
            method = getattr(target, make_action)
            signature = inspect.signature(method)
            # Validate parameters count
            required_params = [
                p for p in signature.parameters.values()
                if p.default == inspect.Parameter.empty
                and p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            ]
            if len(parameters) != len(required_params):
                messagebox.showerror("Ошибка", f"Метод '{make_action}' ожидает {len(required_params)} обязательных параметров, передано {len(parameters)}")
                return False
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка валидации: {e}")
            return False
        return True
    # Save commands data to JSON file with backup
    def _save_commands_data(self, commands_data):
        directory = os.path.dirname(self.COMMANDS_FILE)
        if directory:
            os.makedirs(directory, exist_ok=True)
        # Save with backup
        temp_file = self.COMMANDS_FILE + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(commands_data, file, ensure_ascii=False, indent=4)
        # Replace original file
        os.replace(temp_file, self.COMMANDS_FILE)
        # Update assistant commands
        self.assistant.commands = commands_data.get("commands", [])
        self.assistant.activation_words = commands_data.get("activation", [])
    # Add command to JSON file
    def add_command_to_json(self, new_command):
        try:
            # Load existing data
            if os.path.exists(self.COMMANDS_FILE):
                with open(self.COMMANDS_FILE, "r", encoding="utf-8") as file:
                    commands_data = json.load(file)
            else:
                commands_data = {"activation": [], "commands": []}
            commands_data.setdefault("activation", [])
            commands_data.setdefault("commands", [])
            # Add new command
            commands_data["commands"].append(new_command)
            self._save_commands_data(commands_data)
            logging.info("Команда '%s' успешно добавлена", new_command["command"])
        except Exception as e:
            logging.error("Ошибка добавления команды: %s", e)
            raise
    # Edit existing command
    def edit_command(self):
        command_name = self.selected_command_name
        if not command_name:
            messagebox.showwarning("Предупреждение", "Сначала выберите команду для редактирования")
            return
        try:
            with open(self.COMMANDS_FILE, "r", encoding="utf-8") as file:
                commands_data = json.load(file)
            # Find command to edit
            command_to_edit = next((cmd for cmd in commands_data["commands"] if cmd.get("command") == command_name), None)
            if not command_to_edit:
                messagebox.showerror("Ошибка", f"Команда '{command_name}' не найдена")
                return
            # Create edit dialog
            dialog, content = self.create_command_dialog(f"Редактирование: {command_name}")
            # Fill fields with existing data
            command_entry = self.create_dialog_field(content, "Название команды:", value=command_to_edit.get("command", ""))
            triggers_entry = self.create_dialog_field(content, "Триггеры (через запятую):", value=", ".join(command_to_edit.get("triggers", [])))
            make_entry = self.create_dialog_field(content, "Действие:", value=command_to_edit.get("make", ""))
            handler_var = self.create_handler_field(content, command_to_edit.get("handler", "self"))
            parameters_entry = self.create_dialog_field(content, "Параметры (через запятую):", value=", ".join(command_to_edit.get("parameters", [])))
            say_entry = self.create_dialog_field(content, "Голосовой ответ:", value=command_to_edit.get("say", ""))
            def save_edited_command():
                try:
                    # Get updated values
                    updated_command = {
                        "command": command_entry.get().strip(),
                        "triggers": [t.strip() for t in triggers_entry.get().split(",") if t.strip()],
                        "make": make_entry.get().strip(),
                        "handler": handler_var.get(),
                        "parameters": [p.strip() for p in parameters_entry.get().split(",") if p.strip()],
                        "say": say_entry.get().strip()
                    }
                    # Validate
                    if not updated_command["command"] or not updated_command["triggers"] or not updated_command["make"]:
                        messagebox.showerror("Ошибка", "Заполните обязательные поля: название, триггеры, действие", parent=dialog)
                        return
                    # Check for name conflicts
                    if not self.validate_command(
                        updated_command["command"],
                        updated_command["make"],
                        updated_command["handler"],
                        updated_command["parameters"],
                        exclude_command=command_name
                    ):
                        return
                    # Update command
                    command_to_edit.update(updated_command)
                    # Save
                    self._save_commands_data(commands_data)
                    # Refresh display
                    self.load_commands()
                    dialog.destroy()
                    logging.info("Команда '%s' успешно обновлена", updated_command["command"])
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}", parent=dialog)
            self.create_dialog_buttons(content, save_edited_command, dialog)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка редактирования: {e}")
    # Delete selected command
    def delete_command(self):
        command_name = self.selected_command_name
        if not command_name:
            messagebox.showwarning("Предупреждение", "Сначала выберите команду для удаления")
            return
        # Confirm deletion
        if not messagebox.askyesno("Подтверждение", f"Удалить команду '{command_name}'?"):
            return
        try:
            # Load and update commands
            with open(self.COMMANDS_FILE, "r", encoding="utf-8") as file:
                commands_data = json.load(file)
            # Remove command
            commands_data["commands"] = [cmd for cmd in commands_data["commands"] if cmd.get("command") != command_name]
            # Save
            self._save_commands_data(commands_data)
            # Refresh display
            self.load_commands()
            logging.info("Команда '%s' удалена", command_name)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления: {e}")
    # Get device name by index
    def get_device_by_index(self, index):
        devices = sd.query_devices()
        if 0 <= index < len(devices):
            return f"{index}: {devices[index]['name']}"
        return None
    # Gets a list of available audio input devices
    def get_input_devices(self):
        devices = sd.query_devices()
        input_devices = []
        for i, device in enumerate(devices):
            if device["max_input_channels"] > 0:
                input_devices.append(f"{i}: {device['name']}")
        return input_devices if input_devices else ["Нет доступных устройств ввода"]
    # Get default device index
    def get_default_input_device(self):
        default_input_device = sd.default.device[0]
        devices = sd.query_devices()
        if 0 <= default_input_device < len(devices):
            return f"{default_input_device}: {devices[default_input_device]['name']}"
        return "Выберите устройство ввода"
    # Saves the selected device and updates it in Assistant
    def save_device(self):
        selected = self.device_combobox.get()
        if selected and selected != "Выберите устройство ввода" and selected != "Нет доступных устройств ввода":
            try:
                self.selected_device = int(selected.split(":")[0])
                self.assistant.set_input_device(self.selected_device)
                logging.info("Выбрано устройство: %s", selected)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить устройство: {e}")
        else:
            logging.info("Устройство не выбрано.")
    # Start the main interface loop
    def start_interface(self):
        self.root.mainloop()