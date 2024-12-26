# 🌐 Voice Assistant in Python

This project implements a voice assistant in Python using object-oriented programming (OOP) principles and composition. The program adheres to flake8 coding standards, which ensures high readability, consistent style, and code quality.

**Program Description:**

The program implements a functional voice assistant capable of recognizing voice commands, performing various tasks, and responding vocally. The assistant leverages several Python libraries for speech recognition, text processing, and voice synthesis, including the following:

**Main Program Functions:**
* **Speech Recognition:** The `vosk` library converts audio input into text.
* **Command Processing:** The `process_command` function in `main.py` analyzes the query, matching it with the `commands_dict` and calling the corresponding method of the `Assistant` class.
* **Command Execution (`Assistant` Class):**
    * `greeting()`: A welcome message.
    * `about()`: Information about the assistant's capabilities.
    * `create_note()`: Creates a text note (with the ability to save it to a file, for example, in `.txt` format).  "This method specifies how notes are stored (file path, file name, naming mechanism to prevent overwriting).
    * `time()`: Displays the current time and date.
    * `music_player()`: Plays a random music file from a specified directory.  Error handling (files not found, incorrect format, etc.) should be implemented.
    * `open_telegram()`: Launches Telegram.  It should be noted that this may require additional libraries or interaction with the operating system.
    * `finish()`: Gracefully terminates the program.
* **Information Retrieval (`NetworkActions` Class):**
    * `web_search()`: Searches Google using `webbrowser` to open the link in a browser. The query is formed by concatenating the search query with the base Google URL. Example: `https://www.google.com/search?q={search_query}`.
    * `wikipedia_search()`: Searches Wikipedia (handling `wikipedia.exceptions.PageError` exceptions when information is missing).
    * `check_searching()`: heck_searching(): Determines the search type based on keywords in the query. It should specify which keywords are used to determine the search type. 
    * `get_city_weather():` Retrieves weather information for a specified city using OpenWeather's API and an API key from the .env file.
    Currently, the voice assistant supports only Russian language.  The complete list of commands is in the file `commands.py`.
* **Speech Synthesis:** `pyttsx3` converts text responses into speech.


**OOP and Composition:**

The project uses composition, where the Assistant class includes objects such as pyttsx3.init() and NetworkActions. This approach offers: <br />

**Flexibility:** Components can be replaced or expanded without altering the Assistant class.<br />
**Modularity:** Each component has a distinct responsibility, improving maintainability and readability.<br />
**Reusability:** Components can be reused in other projects or features.<br />
**Simplified Testing:** Each component can be tested independently.<br />

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
python 3.11.9  <br />
