'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
# Installing the necessary libraries
import queue
import vosk
import datetime
import os
import pygame
import sounddevice as sd
import pyttsx3
import json
from rapidfuzz import fuzz
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
        # Load commands from JSON file
        with open('commands.json', 'r', encoding='utf-8') as file:
            commands_data = json.load(file)
            self.commands = commands_data['commands']
            self.activation_words = commands_data['activation']

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
        self.audio_queue = queue.Queue()
        self.is_listening = False

    def play_startup_sound(self):
        """AI is creating summary for play_startup_sound
        """
        # Replace with your MP3 file path
        startup_file = 'sounds/start.mp3'
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

    # Constantly listens to ambient sounds while waiting for the activation word
    def listen_for_activation(self):
        """AI is creating summary for listen_for_activation
        """
        device = sd.default.device
        samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
        rec = vosk.KaldiRecognizer(self.model, samplerate)

        # Callback function for the audio stream. It is called whenever new audio data is available
        def callback(indata, frames, time, status):
            if status:
                print(status)
                # Add the incoming audio data to the queue for processing
            self.audio_queue.put(bytes(indata))
            # Start recording audio in a continuous stream
        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device[0],
                               dtype='int16', channels=1, callback=callback):
            # Notify that the assistant is waiting for the keyword
            print("Ожидание активационного слова 'Астра'...")
            while True:
                # Get the next chunk of audio data from the queue
                data = self.audio_queue.get()
                # Process the audio data with the Vosk recognizer
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    recognized_text = json.loads(result)['text'].lower()
                    # Check if the activation keyword 'Астра' is in the recognized text
                    if any(word in recognized_text for word in self.activation_words):
                        # Notify that the keyword was detected
                        print("Активационное слово распознано.")
                        self.is_listening = True
                        self.speak("Слушаю...")
                        break
                else:
                    print(rec.PartialResult())

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

    # Runs the file on the specified path
    def start_file(self, file_path):
        """AI is creating summary for start_file

        Args:
            file_path ([type]): [description]
        """
        if os.path.isfile(file_path):
            try:
                os.startfile(file_path)
            except Exception as e:
                self.speak(f"Ошибка при открытии файла: {e}")
        else:
            self.speak(f"Файл '{file_path}' не найден.")

    def process_command(self, query):
        """AI is creating summary for process_command

        Args:
            query ([type]): [description]
        """
        best_match = None
        best_score = 0

        # Going through all the commands from JSON
        for cmd in self.commands:
            for trigger in cmd['triggers']:
                score = fuzz.ratio(query, trigger)
                if score > best_score:
                    best_match = cmd
                    best_score = score

        # If a match is found with a high percentage (e.g., above 75)
        if best_match and best_score > 75:
            try:
                # Find and call the method that matches the command, taking into account the parameters
                if hasattr(self.system_control, best_match['make']):
                    method = getattr(self.system_control, best_match['make'])
                elif hasattr(self.network_actions, best_match['make']):
                    method = getattr(self.network_actions, best_match['make'])
                else:
                    method = getattr(self, best_match['make'], None)

                if method:
                    self.speak(best_match['say'])
                    if best_match['parameters']:
                        if best_match['make'] == "hotkey":
                            method(best_match)
                        else:
                            method(*best_match['parameters'])
                    else:
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
            return

        # If no match found, ask ChatGPT for a response
        response = self.chat_gpt.ask(query)
        self.speak(response)

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

    # Requests a music track from the user and plays it using NetworkActions
    def music_player(self):
        """AI is creating summary for music_player
        """
        self.speak("Что будем слушать?")
        query = self.listen_command()
        if query:
            result = self.network_actions.music_player.play_music_request(query)
            self.speak(result)
        else:
            self.speak("Не удалось распознать запрос.")

    # Requests a film from the user and plays it using NetworkActions
    def play_film(self):
        """AI is creating summary for play_film
        """
        self.speak("Что будем смотреть?")
        query = self.listen_command()
        if query:
            result = self.network_actions.film_player.play_film_request(query)
            self.speak(result)
        else:
            self.speak("Не удалось распознать запрос.")

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
        while True:
            self.listen_for_activation()
            while self.is_listening:
                query = self.listen_command()
                if query:
                    self.process_command(query)
                else:
                    self.speak("Пожалуйста, повторите запрос.")
                self.is_listening = False


if __name__ == '__main__':
    assistant = Assistant()
    assistant.main()