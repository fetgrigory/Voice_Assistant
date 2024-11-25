'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
# Installing the necessary libraries
import speech_recognition
import webbrowser
import datetime
import pyttsx3

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка'],
        'open_website': ['открой браузер', 'запусти браузер', 'открой google chrome', 'google chrome'],
        'about': ['кто ты'],
        'time': ['сколько время', 'время', 'текущее время', 'сейчас времени', 'который час']

    }
}


def listen_command():
    # Define the function to listen for and recognize user commands
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio,
                                        language='ru-RU').lower()
        return query
    except speech_recognition.UnknownValueError:
        say_message("Прожуй прежде чем разговаривать")


# Initialize the text-to-speech engine
engine = pyttsx3.init()


def greeting(message):
    message = message.lower()
    if "привет" in message:
        say_message("Привет друг!")
    else:
        say_message("Прожуй прежде чем разговаривать")


def about():
    return say_message('Я Голосовой ассистент создана чтобы служить людям!')


def create_task():
    print('Что добавим в список дел?')
    query = listen_command()
    with open('todo-list.txt', 'a', encoding='utf-8') as file:
        file.write(f'❗️ {query}\n')
    return say_message(f'Задача {query} добавлена в todo-list!')


def time():
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M")
    return say_message(f"Сейчас {formatted_time}")


def open_website():
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open("https://ya.ru/")
    return say_message('Открываю')


# Define the function to speak a message
def say_message(message):
    print(f"Saying: {message}")
    engine.say(message)
    engine.runAndWait()


def main():
    # Initial message
    say_message("Гапуся слушает")
    while True:
        query = listen_command()
        for k, v in commands_dict['commands'].items():
            if query in v:
                print(globals()[k]())


if __name__ == '__main__':
    main()
