'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
# Installing the necessary libraries
import sounddevice as sd
import vosk
import queue
import pyttsx3
import sys

# Initialize a queue for storing audio data
q = queue.Queue()

# Load the Vosk speech recognition model (small model)
model = vosk.Model('vosk-small')

# Get the default microphone device and its sample rate
device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])

# Initialize the text-to-speech engine
engine = pyttsx3.init()


# Define the function to process user commands
def do_this_command(message):
    message = message.lower()
    if "привет" in message:
        say_message("Привет друг!")
    elif "кто ты" in message:
        say_message("Я Голосовой ассистент создан чтобы служить людям!")
    elif "заметка" in message:
        create_task()
    elif "пока" in message:
        say_message("Пока друг!")
        exit()
    else:
        say_message("Прожуй прежде чем разговаривать")


# Define the function to create a new task
def create_task():
    say_message("Что записать?")
    # Start recording user's speech for the note
    listen_command(create_task_callback)


# Define the callback function for create_task
def create_task_callback(recognized_text):
    # Write the recognized text to the file
    with open('todo-list.txt', 'a', encoding='utf-8') as file:
        file.write(f"{recognized_text}\n")
    say_message("Записала!")


# Define the function to speak a message
def say_message(message):
    print(f"Saying: {message}")
    # Turn off the microphone before speaking
    stream.stop()
    engine.say(message)
    engine.runAndWait()
    # Turn on the microphone after the assistant has finished
    stream.start()


# Define the function to listen for and recognize user commands
def listen_command(callback_function):
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000,
                            device=device[0], dtype='int16',
                            channels=1, callback=callback) as stream:
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                text = rec.Result()
                print(text[9:-2])
                recognized_text = text.strip('"')
                callback_function(recognized_text)
                break


# Define the callback function for the audio stream
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


# Create an instance of the audio stream
with sd.RawInputStream(samplerate=samplerate, blocksize=16000,
                        device=device[0], dtype='int16',
                        channels=1, callback=callback) as stream:
    # Create a Vosk recognizer
    rec = vosk.KaldiRecognizer(model, samplerate)
    # Initial message
    say_message("Гапуся слушает")
    # Continuously listen for audio and process it
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            text = rec.Result()
            # Removing curly braces
            print(text[9:-2])
            # Extract the recognized text and process it
            recognized_text = text.strip('"')
            do_this_command(recognized_text)
