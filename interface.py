'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 14/03/2025
Ending //
'''
import customtkinter as ctk
import sounddevice as sd


class VoiceAssistantApp:
    """AI is creating summary for
    """
    def __init__(self, assistant):
        self.assistant = assistant
        self.root = ctk.CTk()
        self.root.title("Голосовой помощник")
        self.root.geometry("600x400")
        self.root.resizable(width=False, height=False)

        # Configuration of the appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        # Selected device
        self.selected_device = None
        self.create_widgets()

        # Status string above
    def create_widgets(self):
        """AI is creating summary for create_widgets
        """
        self.statusbar1 = ctk.CTkLabel(self.root, text="Голосовой помощник", anchor="w", font=('Arial', 16, 'italic'))
        self.statusbar1.pack(side="top", fill="x", padx=10, pady=5)

        # Combobox for selecting sound input devices
        self.device_options = self.get_input_devices()
        # Get default device
        default_device = self.get_default_input_device()
        self.device_combobox = ctk.CTkComboBox(self.root, values=self.device_options, font=('Arial', 14))
        # Default device installation
        self.device_combobox.set(default_device)
        self.device_combobox.pack(padx=10, pady=10)
        # "Save" button
        self.save_button = ctk.CTkButton(self.root, text="Сохранить", command=self.save_device)
        self.save_button.pack(pady=10)
        self.statusbar2 = ctk.CTkLabel(self.root, text="Вход микрофона:", anchor="w", font=('Arial', 16, 'italic'))
        self.update_statusbar2_position()

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
            print(f"Выбрано устройство: {selected}")
        else:
            print("Устройство не выбрано.")

    def update_statusbar2_position(self):
        """AI is creating summary for update_statusbar2_position
        """
        self.root.update_idletasks()
        self.statusbar2.place(x=10, y=self.device_combobox.winfo_y())

    def start_interface(self):
        """AI is creating summary for start_interface
        """
        self.root.mainloop()
