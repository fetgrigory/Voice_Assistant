import inspect
import json
import logging
import os
import tkinter as tk
from contextlib import suppress
from tkinter import messagebox

import customtkinter as ctk

from .styles import (COLORS, FONT, create_button, create_card, create_combobox,
                     create_entry, create_label, create_section_title)


# "Команды" tab: list of voice commands and CRUD operations over commands.json
class CommandsTab:
    COMMANDS_FILE = "src/config/commands.json"
    VALID_HANDLERS = [
        "self",
        "system_control",
        "network_actions",
    ]

    def __init__(self, parent, root, assistant):
        self.tab = parent
        self.root = root
        self.assistant = assistant
        self.selected_command_name = None
        self.commands_data = []
        self.commands_list_textbox = None

        self.create_widgets()
        self.load_commands()

    def create_widgets(self):
        create_section_title(
            self.tab,
            "Управление командами",
            "Создавайте, редактируйте и удаляйте голосовые команды"
        )

        commands_frame = create_card(self.tab)
        commands_frame.pack(fill="both", expand=True, padx=20, pady=(5, 10))

        self.commands_list_textbox = ctk.CTkTextbox(
            commands_frame,
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

        self.commands_list_textbox._textbox.bind("<Button-1>", self._on_command_click, add="+")
        self.commands_list_textbox._textbox.tag_configure("selected", background=COLORS["accent"][0])

        buttons_frame = ctk.CTkFrame(self.tab, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(5, 15))

        create_button(
            buttons_frame, "+  Добавить команду", self.open_add_command_window, 175, "primary"
        ).pack(side="left", padx=(0, 8))
        create_button(
            buttons_frame, "Редактировать", self.edit_command, 145, "secondary"
        ).pack(side="left", padx=8)
        create_button(
            buttons_frame, "Удалить", self.delete_command, 110, "danger"
        ).pack(side="left", padx=8)

    # Selects the command block under the cursor
    def _on_command_click(self, event):
        widget = event.widget
        with suppress(tk.TclError, ValueError):
            index = widget.index(f"@{event.x},{event.y}")
            line_number = int(index.split(".")[0])

            command_name = None
            for line in range(line_number, 0, -1):
                content = widget.get(f"{line}.0", f"{line}.end")
                if content.startswith("Команда: "):
                    command_name = content.replace("Команда: ", "", 1).strip()
                    break

            if command_name and any(cmd.get("command") == command_name for cmd in self.commands_data):
                self.selected_command_name = command_name

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

    def display_commands(self, commands):
        textbox = self.commands_list_textbox
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        self.selected_command_name = None

        if not commands:
            textbox.insert("end", "\n\n          Команды пока не добавлены.\n          Нажмите «Добавить команду», чтобы создать первую.")

        for cmd in commands:
            triggers = ", ".join(cmd.get("triggers", []))
            parameters = ", ".join(cmd.get("parameters", []))
            command_text = (
                f"Команда: {cmd.get('command', '')}\n"
                f"Триггеры: {triggers}\n"
                f"Действие: {cmd.get('make', '')}\n"
                f"Обработчик: {cmd.get('handler', '')}\n"
                f"Параметры: {parameters}\n"
                f"Ответ: {cmd.get('say', '')}\n"
                f"{'─' * 55}\n\n"
            )
            textbox.insert("end", command_text)

        textbox.configure(state="disabled")

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

        card = create_card(dialog)
        card.pack(fill="both", expand=True, padx=20, pady=10)

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)

        return dialog, content

    def create_dialog_field(self, parent, label, placeholder="", value=None):
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=6)

        create_label(field_frame, label).pack(anchor="w", pady=(0, 5))
        entry = create_entry(field_frame, placeholder=placeholder, width=400)
        if value is not None:
            entry.insert(0, str(value))
        entry.pack(fill="x")
        return entry

    def create_handler_field(self, parent, value="self"):
        field_frame = ctk.CTkFrame(parent, fg_color="transparent")
        field_frame.pack(fill="x", pady=6)

        create_label(field_frame, "Обработчик:").pack(anchor="w", pady=(0, 5))
        handler_var = ctk.StringVar(value=value)
        combobox = create_combobox(field_frame, self.VALID_HANDLERS, width=400, height=40, variable=handler_var)
        combobox.pack(fill="x")
        return handler_var

    # Builds the command form: placeholders for a new command, current values when editing
    def create_command_form(self, content, command=None):
        editing = command is not None
        command = command or {}

        def field(label, placeholder, key, is_list=False):
            value = None
            if editing:
                value = command.get(key, [] if is_list else "")
                if is_list:
                    value = ", ".join(value)
            return self.create_dialog_field(content, label, "" if editing else placeholder, value)

        return {
            "command": field("Название команды:", "Например: открыть браузер", "command"),
            "triggers": field("Триггеры (через запятую):", "Например: браузер, открой браузер", "triggers", is_list=True),
            "make": field("Действие:", "Название метода", "make"),
            "handler": self.create_handler_field(content, command.get("handler", "self")),
            "parameters": field("Параметры (через запятую):", "Параметры метода", "parameters", is_list=True),
            "say": field("Голосовой ответ:", "Ответ ассистента", "say"),
        }

    def read_command_form(self, form):
        return {
            "command": form["command"].get().strip(),
            "make": form["make"].get().strip(),
            "handler": form["handler"].get(),
            "parameters": [p.strip() for p in form["parameters"].get().split(",") if p.strip()],
            "say": form["say"].get().strip(),
            "triggers": [t.strip() for t in form["triggers"].get().split(",") if t.strip()],
        }

    def create_dialog_buttons(self, parent, save_command, dialog):
        buttons = ctk.CTkFrame(parent, fg_color="transparent")
        buttons.pack(fill="x", pady=(15, 5))

        create_button(buttons, "Отмена", dialog.destroy, 130, "secondary").pack(side="right", padx=(8, 0))
        create_button(buttons, "Сохранить", save_command, 130, "primary").pack(side="right")

    def open_add_command_window(self):
        dialog, content = self.create_command_dialog("Добавление команды")
        form = self.create_command_form(content)

        def save_command():
            try:
                command = self.read_command_form(form)
                if not self.is_command_valid(command, dialog):
                    return

                self.add_command_to_json(command)
                self.load_commands()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения команды: {e}", parent=dialog)

        self.create_dialog_buttons(content, save_command, dialog)

    def edit_command(self):
        command_name = self.selected_command_name
        if not command_name:
            messagebox.showwarning("Предупреждение", "Сначала выберите команду для редактирования")
            return

        try:
            with open(self.COMMANDS_FILE, "r", encoding="utf-8") as file:
                commands_data = json.load(file)

            command_to_edit = next((cmd for cmd in commands_data["commands"] if cmd.get("command") == command_name), None)
            if not command_to_edit:
                messagebox.showerror("Ошибка", f"Команда '{command_name}' не найдена")
                return

            dialog, content = self.create_command_dialog(f"Редактирование: {command_name}")
            form = self.create_command_form(content, command_to_edit)

            def save_edited_command():
                try:
                    updated_command = self.read_command_form(form)
                    if not self.is_command_valid(updated_command, dialog, exclude_command=command_name):
                        return

                    command_to_edit.update(updated_command)
                    self._save_commands_data(commands_data)

                    self.load_commands()
                    dialog.destroy()
                    logging.info("Команда '%s' успешно обновлена", updated_command["command"])
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}", parent=dialog)

            self.create_dialog_buttons(content, save_edited_command, dialog)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка редактирования: {e}")

    def delete_command(self):
        command_name = self.selected_command_name
        if not command_name:
            messagebox.showwarning("Предупреждение", "Сначала выберите команду для удаления")
            return

        if not messagebox.askyesno("Подтверждение", f"Удалить команду '{command_name}'?"):
            return

        try:
            with open(self.COMMANDS_FILE, "r", encoding="utf-8") as file:
                commands_data = json.load(file)

            commands_data["commands"] = [cmd for cmd in commands_data["commands"] if cmd.get("command") != command_name]
            self._save_commands_data(commands_data)

            self.load_commands()
            logging.info("Команда '%s' удалена", command_name)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления: {e}")

    def is_command_valid(self, command, dialog, exclude_command=None):
        if not command["command"] or not command["triggers"] or not command["make"]:
            messagebox.showerror("Ошибка", "Заполните обязательные поля: название, триггеры, действие", parent=dialog)
            return False

        return self.validate_command(
            command["command"],
            command["make"],
            command["handler"],
            command["parameters"],
            exclude_command=exclude_command
        )

    # Checks name uniqueness, handler, method existence and required parameter count
    def validate_command(self, command_name, make_action, handler, parameters, exclude_command=None):
        if os.path.exists(self.COMMANDS_FILE):
            with suppress(Exception):
                with open(self.COMMANDS_FILE, "r", encoding="utf-8") as file:
                    data = json.load(file)
                for cmd in data.get("commands", []):
                    if cmd.get("command") == command_name and cmd.get("command") != exclude_command:
                        messagebox.showerror("Ошибка", f"Команда с именем '{command_name}' уже существует")
                        return False

        if handler not in self.VALID_HANDLERS:
            messagebox.showerror("Ошибка", f"Некорректный обработчик. Допустимые: {', '.join(self.VALID_HANDLERS)}")
            return False

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

            signature = inspect.signature(getattr(target, make_action))
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

    # Writes to a temp file first, then atomically replaces the original
    def _save_commands_data(self, commands_data):
        directory = os.path.dirname(self.COMMANDS_FILE)
        if directory:
            os.makedirs(directory, exist_ok=True)

        temp_file = self.COMMANDS_FILE + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(commands_data, file, ensure_ascii=False, indent=4)
        os.replace(temp_file, self.COMMANDS_FILE)

        self.assistant.commands = commands_data.get("commands", [])
        self.assistant.activation_words = commands_data.get("activation", [])

    def add_command_to_json(self, new_command):
        try:
            if os.path.exists(self.COMMANDS_FILE):
                with open(self.COMMANDS_FILE, "r", encoding="utf-8") as file:
                    commands_data = json.load(file)
            else:
                commands_data = {"activation": [], "commands": []}

            commands_data.setdefault("activation", [])
            commands_data.setdefault("commands", [])
            commands_data["commands"].append(new_command)

            self._save_commands_data(commands_data)
            logging.info("Команда '%s' успешно добавлена", new_command["command"])
        except Exception as e:
            logging.error("Ошибка добавления команды: %s", e)
            raise
