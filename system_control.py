'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 11/01/2025
Ending //
'''
# Installing the necessary libraries
import os
import platform


class SystemControl:
    """AI is creating summary for
    """
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