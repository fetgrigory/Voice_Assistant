# 🌐 Voice Assistant in Python
Gapusya is a voice assistant designed to execute various commands using STT (Speech-to-Text) and TTS (Text-to-Speech) technologies. It operates offline and does not require connection to cloud services.<br />
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
**main.py** — the main program file. Here, an instance of the assistant is created, and the main loop for processing commands is launched.<br />
**commands.py** — a file with command settings, where keywords for various commands are defined.<br />
**network.py** — a file for interacting with external services, such as Wikipedia search, weather retrieval, and web search <br />

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
python-dotenv 1.0.1 <br />
pyttsx3 2.98  <br />
vosk 0.3.45  <br />
Wikipedia 1.4.0  <br />
RapidFuzz 3.11.0 <br />
python 3.11.9  <br />

# New features that will be added in the future (Information may be updated as needed):
1. Integrate the fuzzy recognition system using the "RapidFuzz" library.  ✅
2. Shut down PC  
3. Restart PC  
4. Sleep mode  
5. Empty recycle bin  
6. Create folder/document
7. Check microphone responsiveness  
8. Increase/decrease/mute volume  
9. Take a screenshot
10. Copy text
11. Paste text
12. Delete selected text
13. Switch language
14. Open videos via voice commands
15. Pause
16. Next video
17. Previous video
18. Rewind backward
19. Fast forward
20. Open the beginning/middle/end of the video
21. Enable/disable subtitles
22. Fullscreen mode
23. Turn sound on/off/increase/decrease
24. Zoom in/zoom out/reset page scale
25. New tab
26. Browser homepage
27. Incognito mode
28. Open next/previous tab
29. Reopen closed tab
30. Integration with the WhatsApp messenger  
31. Support for multiple languages
32. Calculator
33. Windows Settings
34. List of commands
35. File Explorer
36. Task Manager
37. Start menu
38. Run center/menu
39. Close a program
40. Minimize/maximize a program (fully)
41. Partial minimize

# Athor
Fetkulin Grigory <br />
