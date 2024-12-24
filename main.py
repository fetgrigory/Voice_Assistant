'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
# Installing the necessary libraries
import speech_recognition as sr
import datetime
import os
import random
import sounddevice as sd
import torch
from commands import commands_dict
from network import NetworkActions


class Assistant:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    # Class representing a voice assistant that can listen to commands, process them, and respond accordingly
    def __init__(self):
        self.r = sr.Recognizer()
        self.r.pause_threshold = 0.5
        self.network_actions = NetworkActions()

        # Load Silero TTS model
        self.model, self.example_text = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language='ru',
            speaker='v3_1_ru'
        )

    def listen_command(self):
        """AI is creating summary for listen_command

        Returns:
            [type]: [description]
        """
        # Listens for audio input from the microphone
        print("Слушаю...")

        # Define parameters for recording
        fs = 16000  # Sampling frequency
        duration = 5  # Seconds to record

        try:
            # Record audio
            audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
            sd.wait()  # Wait until recording is finished

            # Convert to AudioData for speech recognition
            audio_data = sr.AudioData(audio.tobytes(), fs, 2)

            # Recognize speech using Google Web Speech API
            query = self.r.recognize_google(audio_data, language='ru-RU').lower()
            print("Распознано: " + query)
            return query
        except sr.UnknownValueError:
            self.speak("Команда не распознана, повторите!")
            return None
        except sr.RequestError:
            self.speak("Неизвестная ошибка, проверьте интернет!")
            return None

    def speak(self, message):
        """AI is creating summary for speak

        Args:
            message ([type]): [description]
        """
        print(message)
        audio = self.model.apply_tts(
            text=message,
            speaker='baya',
            sample_rate=48000
        )
        sd.play(audio, samplerate=48000)
        sd.wait()

    def process_command(self, query):
        """AI is creating summary for process_command

        Args:
            query ([type]): [description]
        """
        #  Iterates through the commands dictionary
        for k, v in commands_dict['commands'].items():
            # Checks if any keyword for a command is present in the query
            if any(command in query for command in v):
                try:
                    # Gets the method associated with the command
                    method = getattr(self, k)
                    method()
                except AttributeError:
                    self.speak(f"Команда '{query}' пока не реализована.")
                    return
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
            os.system('C:/Users/Admin/AppData/Roaming/"Telegram Desktop"/Telegram.exe')
            self.speak('Открываю Telegram')
        except Exception as e:
            self.speak(f"Ошибка при открытии Telegram: {e}")

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
