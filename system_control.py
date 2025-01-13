'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 11/01/2025
Ending //
'''
# Installing the necessary libraries
import os
import platform
from win32com.shell import shell, shellcon


class SystemControl:
    """AI is creating summary for
    """
    def empty(self, confirm=False, show_progress=False, sound=True):
        """AI is creating summary for empty

        Args:
            confirm (bool, optional): [description]. Defaults to False.
            show_progress (bool, optional): [description]. Defaults to False.
            sound (bool, optional): [description]. Defaults to True.
        """
        flags = 0
        if not confirm:
            # Disable confirmation dialog
            flags |= shellcon.SHERB_NOCONFIRMATION
        if not show_progress:
            # Disable progress display
            flags |= shellcon.SHERB_NOPROGRESSUI
        if not sound:
            # Turn off sound
            flags |= shellcon.SHERB_NOSOUND
        try:
            # Check if the recycle bin is empty
            stats = shell.SHQueryRecycleBin(None)
            # SHQueryRecycleBin returns a structure with multiple values. To get information
            # about the number of items, use the i64NumItems property from stats.
            if stats[0] == 0:  # stats[0] is the number of items in the recycle bin
                print("Корзина уже пуста.")
                return
            # Clear the recycle bin
            shell.SHEmptyRecycleBin(None, None, flags)
            print("Корзина успешно очищена.")
        except Exception as e:
            print(f"Ошибка при очистке корзины: {e}")

    def shutdown(self):
        """AI is creating summary for shutdown

        Raises:
            NotImplementedError: [description]
        """
        # Get the type of operating system (e.g., Windows, Linux, macOS)
        os_type = platform.system()

        # Check if the operating system is Windows
        if os_type == "Windows":
            # Execute the shutdown command for Windows with a 1-second delay
            os.system("shutdown /s /t 1")
        else:
            # Raise an error for unsupported operating systems
            raise NotImplementedError("Unsupported operating system for shutdown command.")

    def restart(self):
        """AI is creating summary for restart

        Raises:
            NotImplementedError: [description]
        """
        # Get the type of operating system (e.g., Windows, Linux, macOS)
        os_type = platform.system()

        # Check if the operating system is Windows
        if os_type == "Windows":
            # Execute the restart command for Windows with a 1-second delay
            os.system("shutdown /r /t 1")
        else:
            # Raise an error for unsupported operating systems
            raise NotImplementedError("Unsupported operating system for restart command.")

    def sleep(self):
        """AI is creating summary for sleep

        Raises:
            NotImplementedError: [description]
        """
        # Get the type of operating system (e.g., Windows, Linux, macOS)
        os_type = platform.system()
        # If the operating system is Windows, execute the command to put the system into sleep mode
        if os_type == "Windows":
            os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
        else:
            # Raise an error for unsupported operating systems
            raise NotImplementedError("Unsupported operating system for sleep command.")
