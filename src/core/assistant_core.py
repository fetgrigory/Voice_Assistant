import json
import logging
import os
import threading
import time
from pathlib import Path

import pygame
import sounddevice as sd
from rapidfuzz import fuzz

from src.integrations.llm_client import LLMClient
from src.gui.main_window import VoiceAssistantApp
from src.network import NetworkActions
from src.audio.sound_module import SoundPlayer
from src.speech.speech_module import SpeechRecognizer
from src.system.system_control import SystemControl
from src.speech.tts_module import TTS

logger = logging.getLogger(__name__)

SETTINGS_PATH = 'src/config/settings.json'
DEFAULT_ASSISTANT_NAME = 'астра'


class Assistant:
    def __init__(self):
        self.input_device = None
        self.assistant_name = None
        self.activation_words = []

        with open('src/config/commands.json', 'r', encoding='utf-8') as f:
            self.commands = json.load(f)['commands']

        self.load_settings()

        self.tts = TTS()
        self.speech_recognizer = SpeechRecognizer(input_device=self.input_device)
        self.sound_player = SoundPlayer()
        self.network_actions = NetworkActions()
        self.system_control = SystemControl(self.tts.speak, self.speech_recognizer.listen_command)
        self.chat_gpt = LLMClient()

        self.sound_player.play_sound('start')
        self.session_timeout = 15

        self.interface_manager = VoiceAssistantApp(self)
        threading.Thread(target=self.main, daemon=True).start()
        self.interface_manager.start_interface()

    # Set the input device and save the settings
    def set_input_device(self, device_index):
        self.input_device = device_index
        self.speech_recognizer.input_device = device_index
        self.save_settings()
        logging.info("Устройство ввода обновлено на %s", device_index)

    # The assistant name is also the activation word, so both are updated together
    def set_assistant_name(self, name):
        name = name.strip()
        if not name:
            return
        self.apply_assistant_name(name)
        self.save_settings()
        logging.info("Имя ассистента изменено на: %s", name)

    def apply_assistant_name(self, name):
        self.assistant_name = name
        self.activation_words = [name.lower()]

    def save_settings(self):
        settings = {
            'input_device': self.input_device,
            'assistant_name': self.assistant_name
        }
        os.makedirs(os.path.dirname(SETTINGS_PATH), exist_ok=True)
        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)

    def load_settings(self):
        settings = {}
        try:
            with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        except Exception:
            pass

        self.input_device = settings.get('input_device', sd.default.device[0])
        self.apply_assistant_name(settings.get('assistant_name') or DEFAULT_ASSISTANT_NAME)

    # Open the specified file
    def start_file(self, file_path):
        project_root = Path(__file__).resolve().parents[1]

        path = Path(file_path)
        if not path.is_absolute():
            path = project_root / path

        if path.is_file():
            try:
                logger.info("Попытка открыть файл: %s", path)
                os.startfile(str(path))
                logger.info("Файл успешно открыт: %s", path)
            except Exception as e:
                error_msg = f"Ошибка при открытии файла: {e}"
                logger.error(error_msg, exc_info=True)
                self.tts.speak(error_msg)
        else:
            error_msg = f"Файл не найден: {path}"
            logger.warning(error_msg)
            self.tts.speak(error_msg)

    # Stop the assistant
    def finish(self):
        self.sound_player.play_sound('shutdown')
        pygame.time.wait(3000)
        logger.info("Assistant finished")
        exit()

    def music_player(self):
        self.tts.speak("Что будем слушать?")
        query = self.speech_recognizer.listen_command()
        if query:
            result = self.network_actions.music_player.play_music_request(query)
            self.tts.speak(result)
        else:
            self.tts.speak("Не удалось распознать запрос.")

    def play_film(self):
        self.tts.speak("Что будем смотреть?")
        query = self.speech_recognizer.listen_command()
        if query:
            result = self.network_actions.film_player.play_film_request(query)
            self.tts.speak(result)
        else:
            self.tts.speak("Не удалось распознать запрос.")

    # Get and announce the latest news
    def read_news(self):
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

    # Get the weather for the specified city
    def get_city_weather(self):
        self.tts.speak("Укажите город:")
        city = self.speech_recognizer.listen_command()
        if city:
            result = self.network_actions.get_weather(city)
            self.tts.speak(result)
        else:
            self.tts.speak("Не удалось распознать город.")

    # Search the web
    def search_online(self):
        self.network_actions.web_search_service.search_online(self.tts, self.speech_recognizer)

    # Process the user's command
    def process_command(self, query):
        best_match, best_score = None, 0
        for cmd in self.commands:
            for trigger in cmd['triggers']:
                score = fuzz.ratio(query, trigger)
                if score > best_score:
                    best_match, best_score = cmd, score
        if best_match and best_score > 75:
            try:
                handler_map = {
                    "self": self,
                    "system_control": self.system_control,
                    "network_actions": self.network_actions
                }
                handler = handler_map.get(best_match.get('handler', 'self'))
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
        response = self.chat_gpt.ask(query)
        self.tts.speak(response)

    # Run the assistant's main loop
    def main(self):
        while True:
            self.speech_recognizer.listen_for_activation(
                self.activation_words,
                lambda: self.tts.speak("Слушаю")
            )
            last_active_time = time.time()
            while time.time() - last_active_time < self.session_timeout:
                query = self.speech_recognizer.listen_command()
                if query:
                    self.process_command(query)
                    last_active_time = time.time()
            self.sound_player.play_sound('shutdown')