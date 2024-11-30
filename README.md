# 🌐 Voice Assistant in Python

This project implements a voice assistant in Python using object-oriented programming (OOP) and the composition principle.  The choice of composition over inheritance is crucial for ensuring flexibility, maintainability, and scalability of the project.

**Program Description:**

The program implements the functionality of a simple voice assistant capable of recognizing voice commands, performing various actions, and responding vocally.  The libraries used are: `speech_recognition` (speech recognition), `pyttsx3` (speech synthesis), `wikipedia` (Wikipedia information retrieval), and `webbrowser` (opening links in a browser).  Functionality is extensible through the `commands_dict` dictionary in the `commands.py` file.

**Main Program Functions:**

* **Speech Recognition:** `speech_recognition` converts audio input into a text query.
* **Command Processing:** The `process_command` function in `main.py` analyzes the query, matching it with the `commands_dict` and calling the corresponding method of the `Assistant` class.
* **Command Execution (`Assistant` Class):**
    * `greeting()`: A welcome message.
    * `about()`: Information about the assistant's capabilities.
    * `create_note()`: Creates a text note (with the ability to save it to a file, for example, in `.txt` format).  It should specify how notes are stored (file path, file name, naming mechanism to prevent overwriting).
    * `time()`: Displays the current time and date.
    * `music_player()`: Plays a random music file from a specified directory.  Error handling (files not found, incorrect format, etc.) should be implemented.
    * `open_telegram()`: Launches Telegram.  It should be noted that this may require additional libraries or interaction with the operating system.
    * `finish()`: Gracefully terminates the program.
* **Information Retrieval (`NetworkActions` Class):**
    * `web_search()`: Searches Google using `webbrowser` to open the link in a browser. The query is formed by concatenating the search query with the base Google URL. Example: `https://www.google.com/search?q={search_query}`.
    * `wikipedia_search()`: Searches Wikipedia (handling `wikipedia.exceptions.PageError` exceptions when information is missing).
    * `check_searching()`: heck_searching(): Determines the search type based on keywords in the query. It should specify which keywords are used to determine the search type. Currently, the voice assistant supports only Russian.  The complete list of commands is in the file `commands.py`.
* **Speech Synthesis:** `pyttsx3` converts text responses into speech.


**OOP and Composition:**

The project uses **composition** instead of inheritance. The `Assistant` class contains `sr.Recognizer`, `pyttsx3.init()`, and `NetworkActions` objects as attributes. This provides:

* **Flexibility:** The ability to replace or add components without modifying the main `Assistant` class.
* **Modularity:** Each component has its own area of responsibility, which improves code readability and maintainability.
* **Avoids the "fragile base class" problem:** Changes in one component do not affect others.
* **Better Encapsulation:** The internal implementation of the components is hidden from `Assistant`.
* **Code Reusability:** Components can be used in other parts of the project or in other projects.
* **Simplified Testing:** Components are tested independently.

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

3. Run the program with the command:
   ```bash
   python main.py
   ```

## Libraries Used and Language Version
PyAudio 0.2.14  <br />
SpeechRecognition 3.11.0  <br />
pyttsx3 2.98  <br />
wikipedia 1.4.0  <br />
python 3.11.9  <br />
