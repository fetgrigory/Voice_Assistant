'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
# Installing the necessary libraries
import vosk
import datetime
import os
import pygame
import random
import sounddevice as sd
import pyttsx3
from rapidfuzz import process, fuzz
from commands import commands_dict
from network import NetworkActions
from chat_gpt import ChatGPT
from system_control import SystemControl


class Assistant:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    # Class representing a voice assistant that can listen to commands, process them, and respond accordingly
    def __init__(self):
        # Replace with the path to your Vosk model
        self.model = vosk.Model("vosk-model-small-ru-0.22")
        self.network_actions = NetworkActions()
        # Creating an instance of the SystemControl class
        self.system_control = SystemControl(self.speak)
        # Creating an instance of ChatGPT module
        self.chat_gpt = ChatGPT()
        # Initialize pyttsx3 TTS engine
        self.engine = pyttsx3.init()
        # Initialize pygame mixer for playing audio
        pygame.mixer.init()

        # Play the startup MP3 file
        self.play_startup_sound()

    def activate_neural_network(self):
        """AI is creating summary for activate_neural_network
        """
        # Notify the user that the neural network is activated
        self.speak("Нейросеть активирована. Скажите ваш запрос.")
        query = self.listen_command()

        if query:
            # Send the query to ChatGPT and get a response
            response = self.chat_gpt.ask(query)
            self.speak(response)
        else:
            # Notify the user that the query was not recognized
            self.speak("Не удалось распознать запрос.")

    def play_startup_sound(self):
        """AI is creating summary for play_startup_sound
        """
        # Replace with your MP3 file path
        startup_file = 'sounds\start.mp3'
        if os.path.exists(startup_file):
            pygame.mixer.music.load(startup_file)
            pygame.mixer.music.play()
        else:
            print(f"Startup file '{startup_file}' not found.")

    def play_shutdown_sound(self):
        """AI is creating summary for play_shutdown_sound
        """
        shutdown_file = 'sounds/shutdown.mp3'
        if os.path.exists(shutdown_file):
            pygame.mixer.music.load(shutdown_file)
            pygame.mixer.music.play()
        else:
            print(f"Shutdown file '{shutdown_file}' not found.")

    def listen_command(self):
        """AI is creating summary for listen_command

        Returns:
            [type]: [description]
        """
        print("Слушаю...")

        # Set device and samplerate
        device = sd.default.device  # Default device
        # sd.default.device = 1, 3  # Specify your input and output device
        samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  # Get the microphone frequency

        duration = 5  # Seconds to record

        try:
            # Record audio using sounddevice with the selected device and samplerate
            audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
            sd.wait()  # Wait until recording is finished

            # Convert audio to Vosk-compatible format
            rec = vosk.KaldiRecognizer(self.model, samplerate)
            if rec.AcceptWaveform(audio.tobytes()):
                result = rec.Result()  # Get the raw result
                query = result.split('"')[3].lower()  # Extract the recognized text
                print("Распознано: " + query)
                return query
            else:
                self.speak("Не удалось распознать речь.")
                return None
        except Exception as e:
            self.speak(f"Ошибка записи звука: {e}")
            return None

    def speak(self, message):
        """AI is creating summary for speak

        Args:
            message ([type]): [description]
        """
        print(message)
        # Set properties for voice (optional)
        self.engine.setProperty('rate', 200)  # Speed of speech
        self.engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

        # Speak the message
        self.engine.say(message)
        self.engine.runAndWait()

    def process_command(self, query):
        """AI is creating summary for process_command

        Args:
            query ([type]): [description]
        """
        best_match = None
        best_score = 0

        # Dictionary for system commands
        system_command = {
            'empty':  self.system_control.empty,
            'shutdown': self.system_control.shutdown,
            'restart': self.system_control.restart,
            'sleep': self.system_control.sleep,
        }

        # Iterate through all commands and their keywords
        for command, keywords in commands_dict['commands'].items():
            # Find the best match for the current command
            match, score, _ = process.extractOne(query, keywords, scorer=fuzz.ratio)

            # Save the command with the best match
            if score > best_score:
                best_match = command
                best_score = score

        # If a match is found with a high percentage (e.g., above 75)
        if best_match and best_score > 75:
            try:
                # If the command is one of the system commands, call the appropriate method
                if best_match in system_command:
                    system_command[best_match]()
                else:
                    method = getattr(self, best_match, None)
                    if method:
                        method()
                    return
            except AttributeError:
                self.speak(f"Команда '{query}' пока не реализована.")
                return

                # Checks if the query needs a web search
        web_search = self.network_actions.check_searching(query)
        if web_search:
            # Speaks the result of the web search
            self.speak(web_search)
    # If no match found, ask ChatGPT for a response
        response = self.chat_gpt.ask(query)
        self.speak(response)

        # Provides a greeting
    def greeting(self):
        """AI is creating summary for greeting
        """
        self.speak("Привет!")

    # Provides information about the assistant
    def about(self):
        """AI is creating summary for about
        """
        self.speak('Я Голосовой ассистент, создана чтобы служить людям!')

# Creates a new note and saves it to a file
    def create_note(self):
        """AI is creating summary for create_note
        """
        print('Что добавим в список дел?')
        query = self.listen_command()
        if query:
            with open('todo-list.txt', 'a', encoding='utf-8') as file:
                file.write(f' {query}\n')
                now = datetime.datetime.now()
            formatted_datetime = now.strftime("%d.%m.%Y %H:%M:%S")
            self.speak(f'Заметка "{query}" создана от {formatted_datetime}.')

    # Tells the current time
    def time(self):
        """AI is creating summary for time
        """
        now = datetime.datetime.now()
        self.speak("Сейчас " + now.strftime("%H:%M"))

    # Plays a random music file from a specified directory
    def music_player(self):
        """AI is creating summary for music_player
        """
        files = os.listdir('music')
        if files:
            random_file = f'music/{random.choice(files)}'
            os.system(f'start {random_file}')
            self.speak(f'Танцуем под {random_file.split("/")[-1]}')
        else:
            self.speak("В папке 'music' нет файлов.")

        # Opens the Telegram application
    def open_telegram(self):
        """AI is creating summary for open_telegram
        """
        try:
            self.speak('Открываю Telegram')
            os.system('C:/Users/Admin/AppData/Roaming/"Telegram Desktop"/Telegram.exe')
        except Exception as e:
            self.speak(f"Ошибка при открытии Telegram: {e}")

    # Opens the Browser application
    def open_browser(self):
        """AI is creating summary for open_browser
        """
        try:
            self.speak('Открываю браузер')
            os.system('"C:/Program Files/Google/Chrome/Application/chrome.exe"')
        except Exception as e:
            self.speak(f"Ошибка при открытии браузера: {e}")

# Gets the weather for the specified city
    def get_city_weather(self):
        """AI is creating summary for get_city_weather
        """
        self.speak("Укажите город:")
        city = self.listen_command()
        if city:
            result = self.network_actions.get_weather(city)
            self.speak(result)

    # Ends the assistant's operation
    def finish(self):
        """AI is creating summary for finish
        """
        self.speak("Пока!")
        self.play_shutdown_sound()
        pygame.time.wait(3000)
        exit()

    # Starts the main loop of the assistant
    def main(self):
        """AI is creating summary for main
        """
        # Get the username of the logged-in user
        user_name = os.getlogin()
        self.speak(f"Привет, {user_name}! Гапуся слушает.")
        while True:
            query = self.listen_command()
            if query:
                self.process_command(query)


if __name__ == '__main__':
    assistant = Assistant()
    assistant.main()
