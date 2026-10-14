import os
import datetime
import platform
import locale
from win32com.shell import shell, shellcon
import keyboard
import pyperclip


class SystemControl:
    def __init__(self, speak, listen_command):
        self.speak = speak
        self.listen_command = listen_command

    # Get the current time
    def get_current_time(self):
        now = datetime.datetime.now()
        self.speak("Сейчас " + now.strftime("%H:%M"))

    # Get the current date
    def get_current_date(self):
        locale.setlocale(locale.LC_TIME, "Russian_Russia.1251")
        now = datetime.datetime.now()
        day_of_week = now.strftime("%A")
        day_of_month = now.strftime("%d")
        month = now.strftime("%B")
        self.speak(f"Сегодня {day_of_week}, {day_of_month} {month}")

    # Get system information
    def system_info(self):
        uname = platform.uname()
        self.speak(f"У вас установлен:{uname.processor}")

    # Empty the recycle bin
    def empty(self, confirm=False, show_progress=False, sound=True):
        flags = 0
        if not confirm:
            flags |= shellcon.SHERB_NOCONFIRMATION
        if not show_progress:
            flags |= shellcon.SHERB_NOPROGRESSUI
        if not sound:
            flags |= shellcon.SHERB_NOSOUND
        try:
            stats = shell.SHQueryRecycleBin(None)
            if stats[1] == 0:
                self.speak("Корзина уже пуста.")
                return
            shell.SHEmptyRecycleBin(None, None, flags)
            self.speak("Корзина успешно очищена.")
        except Exception as e:
            self.speak(f"Ошибка при очистке корзины: {e}")

    # Shut down the system
    def shutdown(self):
        os_type = platform.system()
        if os_type == "Windows":
            os.system("shutdown /s /t 1")
        else:
            raise NotImplementedError("Unsupported operating system for shutdown command.")

    # Restart the system
    def restart(self):
        os_type = platform.system()
        if os_type == "Windows":
            os.system("shutdown /r /t 1")
        else:
            raise NotImplementedError("Unsupported operating system for restart command.")

    # Put the system to sleep
    def sleep(self):
        os_type = platform.system()
        if os_type == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
        else:
            raise NotImplementedError("Unsupported operating system for sleep command.")

    # Press hotkeys
    def hotkey(self, command):
        try:
            hotkey_str = '+'.join(command["parameters"])
            keyboard.send(hotkey_str)
        except Exception as e:
            self.speak(f"Ошибка при нажатии горячих клавиш: {e}")

    # Type text using the keyboard
    def keyboard_write(self):
        input_str = self.listen_command()
        if input_str:
            try:
                pyperclip.copy(input_str)
                keyboard.write(input_str)
                self.speak("Текст успешно вставлен.")
            except Exception as e:
                self.speak(f"Ошибка при вставке текста: {e}")
        else:
            self.speak("Текст не распознан.")