'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 31/08/2025
Ending //
'''
# Installing the necessary libraries
from .network import NetworkActions
from .music_service import MusicManager
from .film_service import FilmManager
from .web_driver_manager import WebDriverManager

__all__ = [
    "NetworkActions",
    "MusicManager",
    "FilmManager",
    "WebDriverManager"
]
