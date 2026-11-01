import json
import logging
import os
from tkinter import messagebox

import customtkinter as ctk
import sounddevice as sd


# Custom logging handler that writes messages into a CTkTextbox
class TkinterLogHandler(logging.Handler):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox

    # Inserts formatted log records into the textbox safely via Tkinter event loop
    def emit(self, record):
        msg = self.format(record)

        def append():
            self.textbox.configure(state="normal")
            self.textbox.insert("end", msg + "\n")
            self.textbox.see("end")
            self.textbox.configure(state="disabled")

        # Schedule GUI update in the main thread
        self.textbox.after(0, append)


# Graphical interface of the voice assistant
class VoiceAssistantApp:
    def __init__(self, assistant):
        self.assistant = assistant
        self.root = ctk.CTk()
        self.root.title("Голосовой помощник")
        self.root.geometry("800x400")
        self.root.resizable(width=False, height=False)

        # Configure appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Selected audio input device
        self.selected_device = None

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
        self.statusbar2 = None
        self.device_options = None
        self.device_combobox = None
        self.save_button = None
        self.logs_frame = None
        self.log_textbox = None
        self.log_handler = None

        # Create main interface elements
        self.create_widgets()

        # Load and display commands
        self.load_commands()

        # Configure textbox for log output
        self.log_textbox.configure(state="disabled")

    # Create commands management tab
    def create_commands_tab(self):
        # Frame for commands list
        self.commands_frame = ctk.CTkFrame(self.commands_tab)
        self.commands_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Commands list textbox
        self.commands_list_textbox = ctk.CTkTextbox(
            self.commands_frame,
            wrap="word",
            state="disabled"
        )
        self.commands_list_textbox.pack(fill="both", expand=True, padx=5, pady=5)

        # Frame for buttons
        self.commands_buttons_frame = ctk.CTkFrame(self.commands_tab)
        self.commands_buttons_frame.pack(fill="x", padx=10, pady=5)

        # Add command button
        self.add_command_button = ctk.CTkButton(
            self.commands_buttons_frame,
            text="Добавить команду",
            command=self.open_add_command_window
        )
        self.add_command_button.pack(side="left", padx=5)

        # Edit command button
        self.edit_command_button = ctk.CTkButton(
            self.commands_buttons_frame,
            text="Редактировать",
            command=self.edit_command
        )
        self.edit_command_button.pack(side="left", padx=5)

        # Delete command button
        self.delete_command_button = ctk.CTkButton(
            self.commands_buttons_frame,
            text="Удалить",
            command=self.delete_command
        )
        self.delete_command_button.pack(side="left", padx=5)

    # Load commands from JSON and display them
    def load_commands(self):
        try:
            commands_file = 'src/config/commands.json'
            if os.path.exists(commands_file):
                with open(commands_file, 'r', encoding='utf-8') as f:
                    commands_data = json.load(f)
                    self.display_commands(commands_data.get('commands', []))
            else:
                self.display_commands([])
        except Exception as e:
            logging.error("Ошибка загрузки команд: %s", e)
            self.display_commands([])

    # Display commands in the textbox
    def display_commands(self, commands):
        self.commands_list_textbox.configure(state="normal")
        self.commands_list_textbox.delete("1.0", "end")

        for cmd in commands:
            triggers = ", ".join(cmd.get('triggers', []))
            say = cmd.get('say', '')
            parameters = ", ".join(cmd.get('parameters', []))

            command_text = f"Команда: {cmd.get('command', '')}\n"
            command_text += f"Триггеры: {triggers}\n"
            command_text += f"Действие: {cmd.get('make', '')}\n"
            command_text += f"Обработчик: {cmd.get('handler', '')}\n"
            command_text += f"Параметры: {parameters}\n"
            command_text += f"Ответ: {say}\n"
            command_text += "-" * 50 + "\n"

            self.commands_list_textbox.insert("end", command_text)

        self.commands_list_textbox.configure(state="disabled")

    # Open window for adding new command
    def open_add_command_window(self):
        # Create dialog window
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Добавление команды")
        dialog.geometry("400x500")
        dialog.resizable(False, False)

        # Command fields
        ctk.CTkLabel(dialog, text="Название команды:").pack(pady=5)
        command_entry = ctk.CTkEntry(dialog, width=300)
        command_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Триггеры (через запятую):").pack(pady=5)
        triggers_entry = ctk.CTkEntry(dialog, width=300)
        triggers_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Действие:").pack(pady=5)
        make_entry = ctk.CTkEntry(dialog, width=300)
        make_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Обработчик:").pack(pady=5)
        handler_var = ctk.StringVar(value="self")
        handler_combobox = ctk.CTkComboBox(
            dialog,
            values=["self", "system_control", "network_actions"],
            variable=handler_var,
            width=300
        )
        handler_combobox.pack(pady=5)

        ctk.CTkLabel(dialog, text="Параметры (через запятую):").pack(pady=5)
        parameters_entry = ctk.CTkEntry(dialog, width=300)
        parameters_entry.pack(pady=5)

        ctk.CTkLabel(dialog, text="Голосовой ответ:").pack(pady=5)
        say_entry = ctk.CTkEntry(dialog, width=300)
        say_entry.pack(pady=5)

        def save_command():
            try:
                command_name = command_entry.get().strip()
                triggers = [t.strip() for t in triggers_entry.get().split(",") if t.strip()]
                make_action = make_entry.get().strip()
                handler = handler_var.get()
                parameters = [p.strip() for p in parameters_entry.get().split(",") if p.strip()]
                say = say_entry.get().strip()

                if not command_name or not triggers or not make_action:
                    messagebox.showerror("Ошибка", "Заполните обязательные поля: название, триггеры, действие")
                    return

                # Validate command
                if not self.validate_command(command_name, make_action, handler, parameters):
                    messagebox.showerror("Ошибка", "Некорректные параметры команды")
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
                messagebox.showerror("Ошибка", f"Ошибка сохранения команды: {e}")

        # Buttons
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=20)

        save_button = ctk.CTkButton(button_frame, text="Сохранить", command=save_command)
        save_button.pack(side="left", padx=10)

        cancel_button = ctk.CTkButton(button_frame, text="Отмена", command=dialog.destroy)
        cancel_button.pack(side="left", padx=10)

    # Validate command parameters
    def validate_command(self, command_name, make_action, handler, parameters):
        # Check if command name is unique
        commands_file = 'src/config/commands.json'
        if os.path.exists(commands_file):
            try:
                with open(commands_file, 'r', encoding='utf-8') as f:
                    commands_data = json.load(f)
                    for cmd in commands_data.get('commands', []):
                        if cmd.get('command') == command_name:
                            messagebox.showerror("Ошибка", f"Команда с именем '{command_name}' уже существует")
                            return False
            except Exception:
                pass

        # Validate handler
        valid_handlers = ["self", "system_control", "network_actions"]
        if handler not in valid_handlers:
            messagebox.showerror("Ошибка", f"Некорректный обработчик. Допустимые: {', '.join(valid_handlers)}")
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
            else:
                messagebox.showerror("Ошибка", f"Неизвестный обработчик: '{handler}'")
                return False

            if target is None or not hasattr(target, make_action):
                messagebox.showerror("Ошибка", f"Метод '{make_action}' не существует в обработчике '{handler}'")
                return False

            # Validate parameters count (basic check)
            method = getattr(target, make_action)
            import inspect
            sig = inspect.signature(method)
            required_params = len([p for p in sig.parameters.values() if p.default == inspect.Parameter.empty and p.name != 'self'])

            if len(parameters) != required_params:
                messagebox.showerror("Ошибка", f"Метод '{make_action}' ожидает {required_params} параметров, передано {len(parameters)}")
                return False

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка валидации: {e}")
            return False

        return True

    # Add command to JSON file
    def add_command_to_json(self, new_command):
        try:
            commands_file = 'src/config/commands.json'

            # Load existing data
            if os.path.exists(commands_file):
                with open(commands_file, 'r', encoding='utf-8') as f:
                    commands_data = json.load(f)
            else:
                commands_data = {"activation": [], "commands": []}

            # Add new command
            commands_data["commands"].append(new_command)

            # Save with backup
            temp_file = commands_file + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(commands_data, f, ensure_ascii=False, indent=4)

            # Replace original file
            if os.path.exists(commands_file):
                os.remove(commands_file)
            os.rename(temp_file, commands_file)

            # Update assistant commands
            self.assistant.commands = commands_data["commands"]
            self.assistant.activation_words = commands_data["activation"]

            logging.info("Команда '%s' успешно добавлена", new_command['command'])

        except Exception as e:
            logging.error("Ошибка добавления команды: %s", e)
            raise

    # Edit existing command
    def edit_command(self):
        try:
            # Get selected command text
            selected_text = self.commands_list_textbox.get("1.0", "end-1c").strip()
            if not selected_text:
                messagebox.showwarning("Предупреждение", "Выберите команду для редактирования")
                return

            # Parse command name from selection
            lines = selected_text.split('\n')
            command_name = None
            for line in lines:
                if line.startswith("Команда: "):
                    command_name = line.replace("Команда: ", "").strip()
                    break

            if not command_name:
                messagebox.showwarning("Предупреждение", "Не удалось определить имя команды")
                return

            # Load existing commands
            commands_file = 'src/config/commands.json'
            with open(commands_file, 'r', encoding='utf-8') as f:
                commands_data = json.load(f)

            # Find command to edit
            command_to_edit = None
            for cmd in commands_data["commands"]:
                if cmd.get('command') == command_name:
                    command_to_edit = cmd
                    break

            if not command_to_edit:
                messagebox.showerror("Ошибка", f"Команда '{command_name}' не найдена")
                return

            # Create edit dialog
            dialog = ctk.CTkToplevel(self.root)
            dialog.title(f"Редактирование команды: {command_name}")
            dialog.geometry("400x500")
            dialog.resizable(False, False)

            # Fill fields with existing data
            ctk.CTkLabel(dialog, text="Название команды:").pack(pady=5)
            command_entry = ctk.CTkEntry(dialog, width=300)
            command_entry.insert(0, command_to_edit.get('command', ''))
            command_entry.pack(pady=5)

            ctk.CTkLabel(dialog, text="Триггеры (через запятую):").pack(pady=5)
            triggers_entry = ctk.CTkEntry(dialog, width=300)
            triggers_entry.insert(0, ", ".join(command_to_edit.get('triggers', [])))
            triggers_entry.pack(pady=5)

            ctk.CTkLabel(dialog, text="Действие:").pack(pady=5)
            make_entry = ctk.CTkEntry(dialog, width=300)
            make_entry.insert(0, command_to_edit.get('make', ''))
            make_entry.pack(pady=5)

            ctk.CTkLabel(dialog, text="Обработчик:").pack(pady=5)
            handler_var = ctk.StringVar(value=command_to_edit.get('handler', 'self'))
            handler_combobox = ctk.CTkComboBox(
                dialog,
                values=["self", "system_control", "network_actions"],
                variable=handler_var,
                width=300
            )
            handler_combobox.pack(pady=5)

            ctk.CTkLabel(dialog, text="Параметры (через запятую):").pack(pady=5)
            parameters_entry = ctk.CTkEntry(dialog, width=300)
            parameters_entry.insert(0, ", ".join(command_to_edit.get('parameters', [])))
            parameters_entry.pack(pady=5)

            ctk.CTkLabel(dialog, text="Голосовой ответ:").pack(pady=5)
            say_entry = ctk.CTkEntry(dialog, width=300)
            say_entry.insert(0, command_to_edit.get('say', ''))
            say_entry.pack(pady=5)

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
                        messagebox.showerror("Ошибка", "Заполните обязательные поля: название, триггеры, действие")
                        return

                    # Check for name conflicts (excluding current command)
                    for cmd in commands_data["commands"]:
                        if cmd.get('command') == updated_command["command"] and cmd != command_to_edit:
                            messagebox.showerror("Ошибка", f"Команда с именем '{updated_command['command']}' уже существует")
                            return

                    # Update command
                    command_to_edit.update(updated_command)

                    # Save
                    temp_file = commands_file + '.tmp'
                    with open(temp_file, 'w', encoding='utf-8') as f:
                        json.dump(commands_data, f, ensure_ascii=False, indent=4)

                    if os.path.exists(commands_file):
                        os.remove(commands_file)
                    os.rename(temp_file, commands_file)

                    # Update assistant
                    self.assistant.commands = commands_data["commands"]

                    # Refresh display
                    self.load_commands()
                    dialog.destroy()

                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка сохранения: {e}")

            # Buttons
            button_frame = ctk.CTkFrame(dialog)
            button_frame.pack(pady=20)

            save_button = ctk.CTkButton(button_frame, text="Сохранить", command=save_edited_command)
            save_button.pack(side="left", padx=10)

            cancel_button = ctk.CTkButton(button_frame, text="Отмена", command=dialog.destroy)
            cancel_button.pack(side="left", padx=10)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка редактирования: {e}")

    # Delete selected command
    def delete_command(self):
        try:
            # Get selected command text
            selected_text = self.commands_list_textbox.get("1.0", "end-1c").strip()
            if not selected_text:
                messagebox.showwarning("Предупреждение", "Выберите команду для удаления")
                return

            # Parse command name
            lines = selected_text.split('\n')
            command_name = None
            for line in lines:
                if line.startswith("Команда: "):
                    command_name = line.replace("Команда: ", "").strip()
                    break

            if not command_name:
                messagebox.showwarning("Предупреждение", "Не удалось определить имя команды")
                return

            # Confirm deletion
            if not messagebox.askyesno("Подтверждение", f"Удалить команду '{command_name}'?"):
                return

            # Load and update commands
            commands_file = 'src/config/commands.json'
            with open(commands_file, 'r', encoding='utf-8') as f:
                commands_data = json.load(f)

            # Remove command
            commands_data["commands"] = [cmd for cmd in commands_data["commands"] if cmd.get('command') != command_name]

            # Save
            temp_file = commands_file + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(commands_data, f, ensure_ascii=False, indent=4)

            if os.path.exists(commands_file):
                os.remove(commands_file)
            os.rename(temp_file, commands_file)

            # Update assistant
            self.assistant.commands = commands_data["commands"]

            # Refresh display
            self.load_commands()

            logging.info("Команда '%s' удалена", command_name)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка удаления: {e}")

    # Add microphone controls to the mic tab
    def create_widgets(self):
        # Title bar
        self.statusbar1 = ctk.CTkLabel(
            self.root,
            text="Голосовой помощник",
            anchor="w",
            font=('Arial', 16, 'italic')
        )
        self.statusbar1.pack(side="top", fill="x", padx=10, pady=5)

        # Create notebook for tabs
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # Microphone tab
        self.mic_tab = self.notebook.add("Микрофон")

        # Commands tab
        self.commands_tab = self.notebook.add("Команды")
        self.create_commands_tab()

        # Logs List (for displaying assistant logs)
        self.logs_frame = ctk.CTkFrame(self.mic_tab)
        self.logs_frame.pack(side="left", padx=20, pady=20)

        # Logs textbox
        self.log_textbox = ctk.CTkTextbox(
            self.logs_frame,
            width=250,
            height=220,
            wrap="word"
        )
        self.log_textbox.pack()

        # Frame for microphone selection
        self.mic_frame = ctk.CTkFrame(self.mic_tab)
        self.mic_frame.pack(side="top", padx=20, pady=20, anchor="n")

        # Label for microphone
        self.statusbar2 = ctk.CTkLabel(
            self.mic_frame,
            text="Вход микрофона:",
            font=('Arial', 16, 'italic')
        )
        self.statusbar2.pack(side="left", padx=(0, 10))

        # Combobox for selecting sound input devices
        self.device_options = self.get_input_devices()

        # Get default device
        saved_device = self.get_device_by_index(self.assistant.input_device)

        self.device_combobox = ctk.CTkComboBox(
            self.mic_frame,
            values=self.device_options,
            font=('Arial', 14)
        )

        # Default device installation
        self.device_combobox.set(
            saved_device if saved_device else self.get_default_input_device()
        )
        self.device_combobox.pack(side="left")

        # "Save" button
        self.save_button = ctk.CTkButton(
            self.mic_tab,
            text="Сохранить",
            command=self.save_device
        )
        self.save_button.pack(pady=10)

        # Connect logging system to textbox
        self.log_handler = TkinterLogHandler(self.log_textbox)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        self.log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.INFO)

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
            if device['max_input_channels'] > 0:
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
        if selected and selected != "Выберите устройство ввода":
            self.selected_device = int(selected.split(":")[0])
            self.assistant.set_input_device(self.selected_device)
            logging.info("Выбрано устройство: %s", selected)
        else:
            logging.info("Устройство не выбрано.")

    def start_interface(self):
        self.root.mainloop()
