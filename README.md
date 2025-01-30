# 🌐 Voice Assistant in Python
Gapusya is a voice assistant designed to execute various commands using STT (Speech-to-Text) and TTS (Text-to-Speech) technologies. It operates offline and does not require connection to cloud services.<br />
This project implements a voice assistant in Python using object-oriented programming (OOP) and the composition principle. The code adheres to the flake8 style guide, ensuring readability and quality.<br />
The goal of the project is to create a local voice assistant capable of performing various tasks, such as creating notes, playing music, checking the weather, and much more, relying solely on local resources.<br />
# Key Features of the Project:
**Works Offline:** However, an internet connection is required for executing commands related to Wikipedia searches and weather data retrieval.<br />
**No Data Collection:** All data remains on your device without being sent to the cloud.
The project is written in Python using various libraries for speech recognition, speech synthesis, and working with internet resources.
# Technology Stack
**Speech Recognition:**  Vosk (a local speech recognition engine)<br />
**Speech Synthesis (TTS):** pyttsx3 (a local speech synthesizer)<br />
**Command Processing**: A command dictionary based on keywords using Python. <br />
**Wikipedia Information Search**: wikipedia library for searching Wikipedia. <br />
**Weather Retrieval via OpenWeather API**: for obtaining weather information.<br /> 

# Architecture and Code Description
**main.py** — the main program module. Here, an instance of the assistant is created, and the main loop for processing commands is launched.<br />
**commands.py** — a module with command settings, where keywords for various commands are defined.<br />
**network.py** — a module for interacting with external services, such as Wikipedia search, weather retrieval, and web search <br />
**system_control.py** —  a module responsible for executing system-level commands, such as shutting down, restarting, or putting the PC to sleep. It also includes functionality for managing the recycle bin and controlling system volume.<br />
**Code Example:**
```
def get_weather(self, city):
    open_weather_token = os.getenv("OPEN_WEATHER_TOKEN")
    if not open_weather_token:
        return "Ошибка: не задан токен для OpenWeather."
    try:
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru")
        data = r.json()
        if data.get("cod") != 200:
            return f"Ошибка: {data.get('message', 'не удалось получить данные о погоде')}."
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        weather = data["weather"][0]["description"]
        return f"Сейчас в городе {city}: {weather}, температура {temp}°C, ощущается как {feels_like}°C."
    except Exception as e:
        return f"Ошибка при получении данных о погоде: {e}"
```
# Usage
### Setting up a virtual environment and running the program

1. Create a virtual environment to isolate project dependencies.
   Use the command:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
3. Set up your OpenWeather API key in a .env file:
  ```bash
   OPENWEATHER_API_KEY=your_api_key_here
```


4. Run the program with the command:
   ```bash
   python main.py
   ```

## Libraries Used and Language Version
Sounddevice 0.5.1<br />
numpy 2.2.1  <br />
pygame 2.6.1 <br />
python-dotenv 1.0.1 <br />
pyttsx3 2.98  <br />
vosk 0.3.45  <br />
Wikipedia 1.4.0  <br />
RapidFuzz 3.11.0 <br />
python 3.11.9  <br />

# New features that will be added in the future (Information may be updated as needed):
1. Integrate the fuzzy recognition system using the "RapidFuzz" library.  ✅
2. Shut down PC  ✅
3. Restart PC ✅ 
4. Sleep mode  ✅
5. Empty recycle bin ✅
6. ChatGPT ✅
7. Create folder/document
8. Check microphone responsiveness  
9. Increase/decrease/mute volume  
10. Take a screenshot
11. Copy text
12. Paste text
13. Delete selected text
14. Switch language
15. Open videos via voice commands
16. Pause
17. Next video
18. Previous video
19. Rewind backward
20. Fast forward
21. Open the beginning/middle/end of the video
22. Enable/disable subtitles
23. Fullscreen mode
24. Turn sound on/off/increase/decrease
25. Zoom in/zoom out/reset page scale
26. Open browser ✅
27. New tab
28. Incognito mode
29. Open next/previous tab
30. Reopen closed tab
31. Integration with the WhatsApp messenger  
32. Support for multiple languages
33. Calculator
34. Windows Settings
35. List of commands
36. File Explorer
37. Task Manager
38. Start menu
39. Run center/menu
40. Close a program
41. Minimize/maximize a program (fully)
42. Partial minimize

# Athor
Fetkulin Grigory <br />
