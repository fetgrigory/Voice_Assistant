'''
This module make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 27/11/2024
Ending //
'''
# Installing the necessary libraries
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import webbrowser as wb
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class NetworkActions:
    """AI is creating summary for
    """
    def __init__(self):
        # Initialize the music player instance
        self.music_player = None

    # Performs a web search using Google
    def web_search(self, query):
        """AI is creating summary for web_search

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        if query:
            # Opens the Google search URL with the provided query
            wb.open("https://www.google.ru/search?q=" + query)
            # Returns a confirmation message
            return "Ищу информацию по запросу " + query
        else:
            # Returns an error message for empty queries
            return "Я не поняла, что надо искать."

    # Checks the query string to determine the appropriate search method (web only)
    def check_searching(self, query):
        """AI is creating summary for check_searching

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        # Checks if the query contains words like "найди" or "найти", indicating a web search
        if any(word in query for word in ["найди", "найти"]):
            # Removes the keywords
            query = query.replace("найди", "").replace("найти", "").strip()
            # Performs a web search
            return self.web_search(query)
        else:
            return False

# Getting weather information
    def get_weather(self, city):
        """AI is creating summary for get_weather

        Args:
            city ([type]): [description]

        Returns:
            [type]: [description]
        """
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

    def play_music_request(self, query):
        """AI is creating summary for play_music_request

        Args:
            query ([type]): [description]
        """
        # Initialize MusicPlayer only if necessary
        if self.music_player is None:
            self.music_player = MusicPlayer()
        return self.music_player.play_music(query)


class MusicPlayer:
    """AI is creating summary for
    """
    def __init__(self):
        # Do not initialize WebDriver immediately
        self.driver = None

    def setup_driver(self):
        """AI is creating summary for setup_driver

        Returns:
            [type]: [description]
        """
        # Set up Selenium WebDriver with Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def open_search_page(self, query):
        """AI is creating summary for open_search_page

        Args:
            query ([type]): [description]
        """
        # Open the search page with the given query
        self.driver.get(f'https://rus.hitmotop.com/search?q={query}')
        time.sleep(3)

    def click_play_button(self):
        """AI is creating summary for click_play_button
        """
        # Find and click the play button
        play_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "jp-play"))
        )
        if play_button.is_enabled():
            play_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "jp-state-playing"))
        )

    def wait_for_track_to_end(self):
        """AI is creating summary for wait_for_track_to_end
        """
        # Wait until the track finishes playing
        while True:
            player = self.driver.find_element(By.CLASS_NAME, "jp-audio")
            player_class = player.get_attribute("class")
            if "jp-state-playing" not in player_class:
                break
            time.sleep(1)

    def play_music(self, query):
        """AI is creating summary for play_music

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        # Play music based on the given query
        try:
            # Initialize WebDriver only when calling the method
            self.driver = self.setup_driver()
            self.open_search_page(query)
            if "404" in self.driver.title:
                return "Ошибка 404: страница не найдена!"
            self.click_play_button()
            track_name_element = self.driver.find_element(By.CLASS_NAME, "jp-track-info__track")
            artist_name_element = self.driver.find_element(By.CLASS_NAME, "jp-track-info__artist")
            track_name = track_name_element.text.strip()
            artist_name = artist_name_element.text.strip()
            print(f"Музыка начала играть: {artist_name} – {track_name}")
            self.wait_for_track_to_end()
            return f"Трек {artist_name} – {track_name} завершился."
        except Exception as e:
            return f"Ошибка при воспроизведении музыки: {e}"
        finally:
            if self.driver:
                self.driver.quit()
