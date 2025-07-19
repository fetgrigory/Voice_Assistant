'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
# Installing the necessary libraries
import json
import logging
import os
import queue
import pygame
import pyttsx3
import sounddevice as sd
import vosk
from rapidfuzz import fuzz
import time
from chat_gpt import ChatGPT
from interface import VoiceAssistantApp
from network import NetworkActions
from system_control import SystemControl

# Configure logging
logging.basicConfig(
    filename='assistant.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)


class Assistant:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    # Class representing a voice assistant that can listen to commands, process them, and respond accordingly
    def __init__(self):
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        # Load settings
        self.settings_file = 'settings.json'
        self.load_settings()
        # Load commands from JSON file
        with open('commands.json', 'r', encoding='utf-8') as file:
            commands_data = json.load(file)
            self.commands = commands_data['commands']
            self.activation_words = commands_data['activation']

        # Replace with the path to your Vosk model
        self.model = vosk.Model("vosk-model-small-ru-0.22")
        self.network_actions = NetworkActions()
        # Creating an instance of the SystemControl class
        self.system_control = SystemControl(self.speak, self.listen_command)
        # Creating an instance of ChatGPT module
        self.chat_gpt = ChatGPT()
        # Initialize pyttsx3 TTS engine
        self.engine = pyttsx3.init()
        # Initialize pygame mixer for playing audio
        pygame.mixer.init()

        # Play the startup MP3 file
        self.play_sound('start')
        self.audio_queue = queue.Queue()
        self.is_listening = False

        # Initialize and start the interface
        self.interface_manager = VoiceAssistantApp(self)
        self.interface_manager.start_interface()
    def read_news(self):
        """Read news aloud"""
        try:
            self.speak("Вот последние новости")
            news_items = self.network_actions.get_news(count=5)
            
            if not news_items:
                self.speak("Не удалось загрузить новости. Проверьте интернет соединение.")
                return
                
            for i, news in enumerate(news_items, 1):
                self.speak(f"Новость {i}. {news['title']}")
                time.sleep(0.5)
                if news['summary']:
                    self.speak(news['summary'])
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Error reading news: {e}")
            self.speak("Произошла ошибка при чтении новостей")

    # Load saved settings from file
    def load_settings(self):
        """AI is creating summary for load_settings
        """
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                self.input_device = settings.get('input_device', sd.default.device[0])
                self.logger.debug("Settings loaded successfully")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.input_device = sd.default.device[0]
            self.logger.warning("Failed to load settings: %s, using defaults", e)

    # Save current settings to file
    def save_settings(self):
        """AI is creating summary for save_settings
        """
        settings = {
            'input_device': self.input_device
        }
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f)
            self.logger.debug("Settings saved successfully")
        except Exception as e:
            self.logger.error("Failed to save settings: %s", e)

    # Sets the selected input device
    def set_input_device(self, device_index):
        """AI is creating summary for set_input_device

        Args:
            device_index ([type]): [description]
        """
        self.input_device = device_index
        self.save_settings()
        self.logger.info("Input device changed to: %s", device_index)

    def play_sound(self, sound_type):
        """AI is creating summary for play_sound

        Args:
            sound_type ([type]): [description]
        """
        sound_file = f'sounds/{sound_type}.mp3'
        if os.path.exists(sound_file):
            try:
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                self.logger.debug("Played sound: %s", sound_file)
            except Exception as e:
                self.logger.error("Failed to play sound %s: %s", sound_file, e)
        else:
            self.logger.warning("Sound file not found: %s", sound_file)

    # Constantly listens to ambient sounds while waiting for the activation word
    def listen_for_activation(self):
        """AI is creating summary for listen_for_activation
        """
        samplerate = int(sd.query_devices(self.input_device, 'input')['default_samplerate'])
        rec = vosk.KaldiRecognizer(self.model, samplerate)

        # Callback function for the audio stream. It is called whenever new audio data is available
        def callback(indata, frames, time, status):
            if status:
                self.logger.warning("Audio stream status: %s", status)
            # Add the incoming audio data to the queue for processing
            self.audio_queue.put(bytes(indata))
        # Start recording audio in a continuous stream
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=self.input_device,
                             dtype='int16', channels=1, callback=callback):
            # Notify that the assistant is waiting for the keyword
            self.logger.info("Ожидание активационного слова 'Астра'...")
            while True:
                # Get the next chunk of audio data from the queue
                data = self.audio_queue.get()
                # Process the audio data with the Vosk recognizer
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    recognized_text = json.loads(result)['text'].lower()
                    # Check if the activation keyword 'Астра' is in the recognized text
                    if any(word in recognized_text for word in self.activation_words):
                        # Notify that the keyword was detected
                        self.logger.info("Активационное слово распознано.")
                        self.is_listening = True
                        self.speak("Слушаю...")
                        break
                else:
                    self.logger.debug(rec.PartialResult())

    def listen_command(self):
        """AI is creating summary for listen_command

        Returns:
            [type]: [description]
        """
        self.logger.info("Слушаю...")
        # Get the microphone frequency
        samplerate = int(sd.query_devices(self.input_device, 'input')['default_samplerate'])
        duration = 5  # Seconds to record
        try:
            # Record audio using sounddevice with the selected device and samplerate
            audio = sd.rec(int(duration * samplerate),
                          samplerate=samplerate, device=self.input_device, channels=1, dtype='int16')
            sd.wait()  # Wait until recording is finished

            # Convert audio to Vosk-compatible format
            rec = vosk.KaldiRecognizer(self.model, samplerate)
            if rec.AcceptWaveform(audio.tobytes()):
                result = rec.Result()  # Get the raw result
                query = result.split('"')[3].lower()  # Extract the recognized text
                self.logger.info("Recognized: %s", query)
                return query
            else:
                self.speak("Не удалось распознать речь.")
                self.logger.warning("Speech recognition failed")
                return None
        except Exception as e:
            self.speak(f"Ошибка записи звука: {e}")
            self.logger.error("Audio recording error: %s", e)
            return None

    def speak(self, message):
        """AI is creating summary for speak

        Args:
            message ([type]): [description]
        """
        self.logger.info("Speaking: %s", message)
        try:
            # Set properties for voice (optional)
            self.engine.setProperty('rate', 200)  # Speed of speech
            self.engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)
            # Speak the message
            self.engine.say(message)
            self.engine.runAndWait()
        except Exception as e:
            self.logger.error("TTS error: %s", e)

    # Runs the file on the specified path
    def start_file(self, file_path):
        """AI is creating summary for start_file

        Args:
            file_path ([type]): [description]
        """
        if os.path.isfile(file_path):
            try:
                logging.info("Попытка открыть файл: %s", file_path)
                os.startfile(file_path)
                logging.info("Файл успешно открыт: %s", file_path)
            except Exception as e:
                error_msg = f"Ошибка при открытии файла: {e}"
                logging.error(error_msg, exc_info=True)
                self.speak(error_msg)
        else:
            error_msg = f"Файл '{file_path}' не найден."
            logging.warning(error_msg)
            self.speak(error_msg)

    def process_command(self, query):
        """AI is creating summary for process_command

        Args:
            query ([type]): [description]
        """
        self.logger.info("Processing command: %s", query)
        best_match = None
        best_score = 0

        # Going through all the commands from JSON
        for cmd in self.commands:
            for trigger in cmd['triggers']:
                score = fuzz.ratio(query, trigger)
                if score > best_score:
                    best_match = cmd
                    best_score = score

        # If a match is found with a high percentage (e.g., above 75)
        if best_match and best_score > 75:
            try:
                # Create a dictionary to map commands to their respective methods
                command_handlers = {
                    "self": self,
                    "system_control": self.system_control,
                    "network_actions": self.network_actions
                }

                # Get the handler object based on the command source
                handler = command_handlers.get(best_match.get('handler', 'self'))
                # Get the method from the handler object
                method = getattr(handler, best_match['make'], None)

                if method:
                    self.speak(best_match['say'])
                    if best_match['parameters']:
                        if best_match['make'] == "hotkey":
                            method(best_match)
                        else:
                            method(*best_match['parameters'])
                    else:
                        method()
                    return
            except Exception as e:
                self.speak(f"Команда '{query}' пока не реализована.")
                self.logger.error("Command execution error: %s", e)
                return

        # Checks if the query needs a web search
        web_search = self.network_actions.check_searching(query)
        if web_search:
            # Speaks the result of the web search
            self.speak(web_search)
            return

        # If no match found, ask ChatGPT for a response
        response = self.chat_gpt.ask(query)
        self.speak(response)

    # Provides information about the assistant
    def about(self):
        """AI is creating summary for about
        """
        self.speak('Я Голосовой ассистент, создана чтобы служить людям!')
        self.logger.info("Displayed 'about' information")

    # Requests a music track from the user and plays it
    def play_music(self, query):
        """AI is creating summary for play_music

        Args:
            query ([type]): [description]
        """
        result = self.network_actions.music_player.play_music_request(query)
        self.speak(result)
        self.logger.info("Music play request: %s", query)

    def music_player(self):
        """AI is creating summary for music_player
        """
        self.speak("Что будем слушать?")
        query = self.listen_command()
        if query:
            self.play_music(query)
        else:
            self.logger.warning("Music play request failed - no query")

    # Requests a film from the user and plays it using NetworkActions
    def play_film(self):
        """AI is creating summary for play_film
        """
        self.speak("Что будем смотреть?")
        query = self.listen_command()
        if query:
            result = self.network_actions.film_player.play_film_request(query)
            self.speak(result)
        else:
            self.speak("Не удалось распознать запрос.")

    # Gets the weather for the specified city
    def get_city_weather(self):
        """AI is creating summary for get_city_weather
        """
        self.speak("Укажите город:")
        city = self.listen_command()
        if city:
            result = self.network_actions.get_weather(city)
            self.speak(result)
            self.logger.info("Weather request for city: %s", city)
        else:
            self.logger.warning("Weather request failed - no city specified")

    # Ends the assistant's operation
    def finish(self):
        """AI is creating summary for finish
        """
        self.play_sound('shutdown')
        pygame.time.wait(3000)
        self.logger.info("PC shutdown")
        exit()

    # Starts the main loop of the assistant
    def main(self):
        """AI is creating summary for main
        """
        self.logger.info("Starting main assistant loop")
        while True:
            self.listen_for_activation()
            while self.is_listening:
                query = self.listen_command()
                if query:
                    self.process_command(query)
                else:
                    self.speak("Пожалуйста, повторите запрос.")
                self.is_listening = False


if __name__ == '__main__':
    assistant = Assistant()
    assistant.main()
