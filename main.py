'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
# Installing the necessary libraries
import speech_recognition as sr
import datetime
import pyttsx3
import os
import random
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
        self.speak_engine = pyttsx3.init()
        self.network_actions = NetworkActions()

    def listen_command(self):
        """AI is creating summary for listen_command

        Returns:
            [type]: [description]
        """
        with sr.Microphone() as source:
            # Listens for audio input from the microphone
            print("Слушаю...")
            audio = self.r.listen(source)
            try:
                # Transcribes the audio using Google Speech Recognition
                query = self.r.recognize_google(audio_data=audio, language='ru-RU').lower()
                print("Распознано: " + query)
                return query
            except sr.UnknownValueError:
                self.speak("Команда не распознана, повторите!")
                return None
            except sr.RequestError:
                print("Неизвестная ошибка, проверьте интернет!")
                return None

    def speak(self, message):
        """AI is creating summary for speak

        Args:
            message ([type]): [description]
        """
        # Speaks the given message using the text-to-speech engine
        print(message)
        # Sends the message to the text-to-speech engine
        self.speak_engine.say(message)
        self.speak_engine.runAndWait()
        self.speak_engine.stop()

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
        self.speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

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
        """AI is creating summary for get_weather
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
