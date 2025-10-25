'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 31/08/2025
Ending //
'''
# Installing the necessary libraries
import logging
import json
import time
import os
import sounddevice as sd
import pygame
from rapidfuzz import fuzz
from chat_gpt import ChatGPT
from interface import VoiceAssistantApp
from network import NetworkActions
from sound_module import SoundPlayer
from speech_module import SpeechRecognizer
from system_control import SystemControl
from tts_module import TTS

logger = logging.getLogger(__name__)


# Main assistant class
class Assistant:
    """AI is creating summary for
    """
    def __init__(self):
        self.settings_file = 'settings.json'
        self.load_settings()

        # Load commands
        with open('commands.json', 'r', encoding='utf-8') as f:
            commands_data = json.load(f)
            self.commands = commands_data['commands']
            self.activation_words = commands_data['activation']

        # Initialize modules
        self.tts = TTS()
        self.speech_recognizer = SpeechRecognizer(input_device=self.input_device)
        self.sound_player = SoundPlayer()
        self.network_actions = NetworkActions()
        self.system_control = SystemControl(self.tts.speak, self.speech_recognizer.listen_command)
        self.chat_gpt = ChatGPT()

        # Startup sound
        self.sound_player.play_sound('start')

        # Interface
        self.interface_manager = VoiceAssistantApp(self)
        self.interface_manager.start_interface()
        # Duration of active session before timeout
        self.session_timeout = 15

    def load_settings(self):
        """AI is creating summary for load_settings
        """
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                self.input_device = settings.get('input_device', sd.default.device[0])
        except Exception:
            self.input_device = sd.default.device[0]

    def save_settings(self):
        """AI is creating summary for save_settings
        """
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump({'input_device': self.input_device}, f)

    # Command methods
    def start_file(self, file_path):
        """AI is creating summary for start_file

        Args:
            file_path ([type]): [description]
        """
        if os.path.isfile(file_path):
            try:
                logger.info("Попытка открыть файл: %s", file_path)
                os.startfile(file_path)
                logger.info("Файл успешно открыт: %s", file_path)
            except Exception as e:
                error_msg = f"Ошибка при открытии файла: {e}"
                logger.error(error_msg, exc_info=True)
                self.tts.speak(error_msg)
        else:
            error_msg = f"Файл '{file_path}' не найден."
            logger.warning(error_msg)
            self.tts.speak(error_msg)

    def about(self):
        """AI is creating summary for about
        """
        self.tts.speak('Я голосовой ассистент, созданный чтобы служить людям!')

    # Ends the assistant's operation
    def finish(self):
        """AI is creating summary for finish
        """
        self.sound_player.play_sound('shutdown')
        pygame.time.wait(3000)
        logger.info("Assistant finished")
        exit()

    def music_player(self):
        """AI is creating summary for music_player
        """
        self.tts.speak("Что будем слушать?")
        query = self.speech_recognizer.listen_command()
        if query:
            result = self.network_actions.music_player.play_music_request(query)
            self.tts.speak(result)
        else:
            self.tts.speak("Не удалось распознать запрос.")

    def play_film(self):
        """AI is creating summary for play_film
        """
        self.tts.speak("Что будем смотреть?")
        query = self.speech_recognizer.listen_command()
        if query:
            result = self.network_actions.film_player.play_film_request(query)
            self.tts.speak(result)
        else:
            self.tts.speak("Не удалось распознать запрос.")

    # Handle news request and announcement
    def read_news(self):
        """AI is creating summary for read_news
        """
        try:
            news_items = self.network_actions.get_latest_news()
            if not news_items:
                self.tts.speak("Не удалось получить новости. Попробуйте позже.")
                return

            self.tts.speak("Вот последние новости:")
            for idx, item in enumerate(news_items, 1):
                self.tts.speak(f"Новость {idx}. {item['title']}")
                time.sleep(0.3)
                if item.get('summary'):
                    self.tts.speak(item['summary'])
                time.sleep(0.5)
        except Exception as e:
            logger.error("Error in news handling: %s", e)

    # Gets the weather for the specified city
    def get_city_weather(self):
        """AI is creating summary for get_city_weather
        """
        self.tts.speak("Укажите город:")
        city = self.speech_recognizer.listen_command()
        if city:
            result = self.network_actions.get_weather(city)
            self.tts.speak(result)
        else:
            self.tts.speak("Не удалось распознать город.")

    # Search online function
    def search_online(self):
        """AI is creating summary for search_online
        """
        self.network_actions.web_search_service.search_online(self.tts, self.speech_recognizer)

    # Command processor
    def process_command(self, query):
        """AI is creating summary for process_command

        Args:
            query ([type]): [description]
        """
        best_match, best_score = None, 0
        for cmd in self.commands:
            for trigger in cmd['triggers']:
                score = fuzz.ratio(query, trigger)
                if score > best_score:
                    best_match, best_score = cmd, score
        # If a match is found with a high percentage (e.g., above 75)
        if best_match and best_score > 75:
            try:
                # Create a dictionary to map commands to their respective methods
                handler_map = {
                    "self": self,
                    "system_control": self.system_control,
                    "network_actions": self.network_actions
                }
                # Get the handler object based on the command source
                handler = handler_map.get(best_match.get('handler', 'self'))
                # Get the method from the handler object
                method = getattr(handler, best_match['make'], None)
                if method:
                    if best_match['say']:
                        self.tts.speak(best_match['say'])
                    if best_match['parameters']:
                        if best_match['make'] == "hotkey":
                            method(best_match)
                        else:
                            method(*best_match['parameters'])
                    else:
                        method()
                    return
            except Exception as e:
                self.tts.speak(f"Команда '{query}' пока не реализована.")
                logger.error("Command execution error: %s", e)
            return
        # If no match found, ask ChatGPT for a response
        response = self.chat_gpt.ask(query)
        self.tts.speak(response)

    # Starts the main loop of the assistant
    def main(self):
        """AI is creating summary for main
        """
        while True:
            # Waiting for the activation word to start the session
            self.speech_recognizer.listen_for_activation(
                self.activation_words,
                lambda: self.tts.speak("Слушаю")
            )
            # Setting the session start time
            last_active_time = time.time()
            # Active session: listening to commands before timeout
            while time.time() - last_active_time < self.session_timeout:
                query = self.speech_recognizer.listen_command()
                if query:
                    self.process_command(query)
                    last_active_time = time.time()
            # Session timeout — play shutdown sound
            self.sound_player.play_sound('shutdown')
