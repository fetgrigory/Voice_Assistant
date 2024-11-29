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
    def __init__(self):
        self.r = sr.Recognizer()
        self.r.pause_threshold = 0.5
        self.speak_engine = pyttsx3.init()
        self.network_actions = NetworkActions()

    def listen_command(self):
        with sr.Microphone() as source:
            print("Слушаю...")
            audio = self.r.listen(source)
            try:
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
        print(message)
        self.speak_engine.say(message)
        self.speak_engine.runAndWait()
        self.speak_engine.stop()

    def process_command(self, query):
        for k, v in commands_dict['commands'].items():
            if any(command in query for command in v):
                try:
                    method = getattr(self, k)
                    method()
                except AttributeError:
                    self.speak(f"Команда '{query}' пока не реализована.")
                    return
                return

        wiki_result = self.network_actions.check_searching(query)
        if wiki_result:
            self.speak(wiki_result)

    def greeting(self):
        self.speak("Привет друг!")

    def about(self):
        self.speak('Я Голосовой ассистент, создана чтобы служить людям!')

    def create_note(self):
        print('Что добавим в список дел?')
        query = self.listen_command()
        if query:
            with open('todo-list.txt', 'a', encoding='utf-8') as file:
                file.write(f' {query}\n')
                now = datetime.datetime.now()
            formatted_datetime = now.strftime("%d.%m.%Y %H:%M:%S")
            self.speak(f'Заметка "{query}" создана от {formatted_datetime}.')

    def time(self):
        now = datetime.datetime.now()
        self.speak("Сейчас " + str(now.hour) + ":" + str(now.minute))

    def music_player(self):
        files = os.listdir('music')
        if files:
            random_file = f'music/{random.choice(files)}'
            os.system(f'start {random_file}')
            self.speak(f'Танцуем под {random_file.split("/")[-1]}')
        else:
            self.speak("В папке 'music' нет файлов.")

    def open_telegram(self):
        try:
            os.system('C:/Users/Admin/AppData/Roaming/"Telegram Desktop"/Telegram.exe')
            self.speak('Открываю Telegram')
        except Exception as e:
            self.speak(f"Ошибка при открытии Telegram: {e}")

    def main(self):
        self.speak("Гапуся слушает")
        while True:
            query = self.listen_command()
            if query:
                self.process_command(query)


if __name__ == '__main__':
    assistant = Assistant()
    assistant.main()
