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
import random
import sounddevice as sd
import pyttsx3
from rapidfuzz import process, fuzz
from commands import commands_dict
from network import NetworkActions
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
        self.system_control = SystemControl()

        # Initialize pyttsx3 TTS engine
        self.engine = pyttsx3.init()

    def listen_command(self):
        """AI is creating summary for listen_command

        Returns:
            [type]: [description]
        """
        print("Слушаю...")

        # Define parameters for recording
        fs = 16000  # Sampling frequency
        duration = 5  # Seconds to record

        try:
            # Record audio using sounddevice
            audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()  # Wait until recording is finished

            # Convert audio to Vosk-compatible format
            rec = vosk.KaldiRecognizer(self.model, fs)
            if rec.AcceptWaveform(audio.tobytes()):
                result = rec.Result()  # Get the raw result
                query = result.split('"')[3].lower()  # Extract the recognized text
                print("Распознано: " + query)
                return query
            else:
                print("Не удалось распознать речь.")
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
                    elif best_match == 'search_wikipedia':
                        wiki_result = self.network_actions.wikipedia_search(query)
                        if wiki_result:
                            self.speak(wiki_result)
                    return
            except AttributeError:
                self.speak(f"Команда '{query}' пока не реализована.")
                return

                # Checks if the query needs a web search
        wiki_result = self.network_actions.check_searching(query)
        if wiki_result:
            # Speaks the result of the web search
            self.speak(wiki_result)

        # Provides a greeting
    def greeting(self):
        """AI is creating summary for greeting
        """
        self.speak("Привет друг!")

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
        self.speak(" Пока, друг!")
        exit()

    # Starts the main loop of the assistant
    def main(self):
        """AI is creating summary for main
        """
        self.speak("Привет, друг! Гапуся слушает.")
        while True:
            query = self.listen_command()
            if query:
                self.process_command(query)


if __name__ == '__main__':
    assistant = Assistant()
    assistant.main()
