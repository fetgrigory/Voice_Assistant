'''
This program makes a simple voice assistant.
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
import speech_recognition as sr
import pyttsx3
sr.pause_threshold = 5

commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка']
    }
}

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.record(source, duration=5)  # Capture audio for 5 seconds
        try:
            recognized_text = r.recognize_google(audio_data=audio, language='ru-RU').lower()
            print(f"You said: {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            print("Не поняла")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None



# Initialize the text-to-speech engine
engine = pyttsx3.init()


# Define the function to process user commands
def greeting(message):
    message = message.lower()
    if "привет" in message:
        say_message("Привет друг!")
    else:
        say_message("Не понял")


def create_task(query): 
    print('Что добавим в список дел?')
    with open('todo-list.txt', 'a', encoding='utf-8') as file:
        file.write(f'❗️ {query}\n')
    return f'Задача {query} добавлена в todo-list!'


# Define the function to speak a message
def say_message(message):
    print(f"Saying: {message}")
    engine.say(message)
    engine.runAndWait()


def main():
    query = listen_command()
    if query is not None:
        for k, v in commands_dict['commands'].items():
            if query in v:
                globals()[k](query)
                break


if __name__ == '__main__':
    main()