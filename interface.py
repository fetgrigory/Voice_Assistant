'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 14/03/2025
Ending //
'''
# Import required libraries
import logging
import customtkinter as ctk
import sounddevice as sd


# Custom logging handler that writes messages into a CTkTextbox
class TkinterLogHandler(logging.Handler):
    """AI is creating summary for TkinterLogHandler

    Args:
        logging ([type]): [description]
    """
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox

# Inserts formatted log records into the textbox safely via Tkinter event loop
    def emit(self, record):
        """AI is creating summary for emit

        Args:
            record ([type]): [description]
        """
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
    """AI is creating summary for
    """
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

        # Create main interface elements
        self.create_widgets()

        # Configure textbox for log output
        self.log_textbox.configure(state="disabled")

        # Connect logging system to textbox
        self.log_handler = TkinterLogHandler(self.log_textbox)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.log_handler.setFormatter(formatter)
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.INFO)

    def create_widgets(self):
        """AI is creating summary for create_widgets
        """
        # Title bar
        self.statusbar1 = ctk.CTkLabel(
            self.root,
            text="Голосовой помощник",
            anchor="w",
            font=('Arial', 16, 'italic')
        )
        self.statusbar1.pack(side="top", fill="x", padx=10, pady=5)

        # Logs List (for displaying assistant logs)
        self.logs_frame = ctk.CTkFrame(self.root)
        self.logs_frame.pack(side="left", padx=20, pady=20)

        self.log_textbox = ctk.CTkTextbox(
            self.logs_frame,
            width=250,
            height=220
        )
        self.log_textbox.pack()

        # Frame for microphone selection
        self.mic_frame = ctk.CTkFrame(self.root)
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
        self.device_combobox.set(saved_device if saved_device else self.get_default_input_device())
        self.device_combobox.pack(side="left")
        # "Save" button
        self.save_button = ctk.CTkButton(
            self.root,
            text="Сохранить",
            command=self.save_device
        )
        self.save_button.pack(pady=10)

    # Get device name by index
    def get_device_by_index(self, index):
        """AI is creating summary for get_device_by_index

        Args:
            index ([type]): [description]

        Returns:
            [type]: [description]
        """
        devices = sd.query_devices()
        if 0 <= index < len(devices):
            return f"{index}: {devices[index]['name']}"
        return None

    # Gets a list of available audio input devices
    def get_input_devices(self):
        """AI is creating summary for get_input_devices

        Returns:
            [type]: [description]
        """
        devices = sd.query_devices()
        input_devices = []
        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                input_devices.append(f"{i}: {device['name']}")
        return input_devices if input_devices else ["Нет доступных устройств ввода"]

    # Get default device index
    def get_default_input_device(self):
        """AI is creating summary for get_default_input_device

        Returns:
            [type]: [description]
        """
        default_input_device = sd.default.device[0]
        devices = sd.query_devices()
        if 0 <= default_input_device < len(devices):
            return f"{default_input_device}: {devices[default_input_device]['name']}"
        return "Выберите устройство ввода"

    # Saves the selected device and updates it in Assistant
    def save_device(self):
        """AI is creating summary for save_device
        """
        selected = self.device_combobox.get()
        if selected and selected != "Выберите устройство ввода":
            self.selected_device = int(selected.split(":")[0])
            self.assistant.set_input_device(self.selected_device)
            logging.info("Выбрано устройство: %s", selected)
        else:
            logging.info("Устройство не выбрано.")

    def update_statusbar2_position(self):
        """AI is creating summary for update_statusbar2_position
        """
        self.root.update_idletasks()
        self.statusbar2.place(x=350, y=self.device_combobox.winfo_y())

    def start_interface(self):
        """AI is creating summary for start_interface
        """
        self.root.mainloop()
