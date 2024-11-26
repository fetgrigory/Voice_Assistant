'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
# Installing the necessary libraries
import speech_recognition
import webbrowser as wb
import datetime
import pyttsx3
import os
import random
from commands import commands_dict
sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5


def listen_command():
    # Define the function to listen for and recognize user commands
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio,
                                        language='ru-RU').lower()
            print("Распознано: " + query)
        return query
    except speech_recognition.UnknownValueError:
        speak("Команда не распознана, повторите!")
    except speech_recognition.RequestError:
        print("Неизвестная ошибка, проверьте интернет!")


# Initialize the text-to-speech engine
speak_engine = pyttsx3.init()


def greeting(message):
    message = message.lower()
    if "привет" in message:
        speak("Привет друг!")
    else:
        speak("Команда не распознана, повторите!")


def about():
    return speak('Я Голосовой ассистент создана чтобы служить людям!')


def create_note():
    print('Что добавим в список дел?')
    query = listen_command()
    with open('todo-list.txt', 'a', encoding='utf-8') as file:
        file.write(f' {query}\n')
        now = datetime.datetime.now()
    formatted_datetime = now.strftime("%d.%m.%Y %H:%M:%S")
    return speak(f'Заметка "{query}" создана от {formatted_datetime}.')


def time():
    # Tell the current time
    now = datetime.datetime.now()
    speak("Сейчас " + str(now.hour) + ":" + str(now.minute))


def music_player():
    files = os.listdir('music')
    # Using os.system to start the sound
    random_file = f'music/{random.choice(files)}'
    os.system(f'start {random_file}')
    return speak(f'Танцуем под {random_file.split("/")[-1]}')


def search_engine():
    speak('Что искать?')
    query = listen_command()
    wb.open('https://www.google.ru/search?q=' + query)
    return speak('Сейчас найду')


def open_website():
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    wb.get(chrome_path).open("https://ya.ru/")
    return speak('Открываю')


def open_telegram():
    os.system('C:/Users/Admin/AppData/Roaming/"Telegram Desktop"/Telegram.exe')
    return speak('Открываю')


# Define the function to speak a message
def speak(message):
    print(message)
    speak_engine.say(message)
    speak_engine.runAndWait()
    speak_engine.stop()


def main():
    # Initial message
    speak("Гапуся слушает")
    while True:
        query = listen_command()
        for k, v in commands_dict['commands'].items():
            if query in v:
                print(globals()[k]())


if __name__ == '__main__':
    main()
