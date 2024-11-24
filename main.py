'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
import os
import random
import speech_recognition
import webbrowser
import datetime

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка'],
        'open_website': ['открой браузер'],
        'about': ['кто ты'],
        'time': ['сколько время']

    }
}


def listen_command():
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio,
                                        language='ru-RU').lower()
        return query
    except speech_recognition.UnknownValueError:
        return 'Damn... Не понял что ты сказал :/'


def greeting():
    return 'Привет друг!'


def about():
    return 'Я Голосовой ассистент создан чтобы служить людям!'


def create_task():
    print('Что добавим в список дел?')
    query = listen_command()
    with open('todo-list.txt', 'a', encoding='utf-8') as file:
        file.write(f'❗️ {query}\n')
    return f'Задача {query} добавлена в todo-list!'


def time():
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M")
    return (f"Сейчас {formatted_time}")


def open_website():
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open("https://ya.ru/")


def main():
    query = listen_command()
    for k, v in commands_dict['commands'].items():
        if query in v:
            print(globals()[k]())


if __name__ == '__main__':
    main()
