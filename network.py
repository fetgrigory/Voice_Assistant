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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import fake_useragent
from selenium.webdriver.chrome.options import Options
import webbrowser as wb
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Config:
    """AI is creating summary for
    """
    # Settings for Music Player
    MUSIC_SEARCH_URL = "https://rus.hitmotop.com/search?q={query}"
    MUSIC_PLAY_BUTTON_CLASS = "jp-play"
    MUSIC_PLAYER_STATE_PLAYING_CLASS = "jp-state-playing"
    PLAYER_AUDIO_CLASS = "jp-audio"
    TRACK_INFO_CLASS = "jp-track-info__track"
    ARTIST_INFO_CLASS = "jp-track-info__artist"

    # Settings for Film Player
    KINOPOISK_URL = "https://www.kinopoisk.ru/"
    SSPOISK_URL_REPLACE = ("kinopoisk.ru", "sspoisk.ru")
    KINOPOISK_CAPTCHA_XPATH = '//*[@id="checkbox-captcha-form"]/div[3]/div/div[1]/div[1]'
    KINOPOISK_SEARCH_INPUT_XPATH = '//*[@id="__next"]/div[1]/div[1]/header/div/div[2]/div[2]/div/form/div/input'
    FIRST_FILM_XPATH = '//div[@class="element most_wanted"]//p[@class="name"]/a'
    IFRAME_TAG = "iframe"
    PLAY_BUTTON_FILM_CLASS = "allplay__controls__item.allplay__control"
    PLAY_BUTTON_PRESSED_CLASS = "allplay__control--pressed"
    FULLSCREEN_BUTTON_ACTION = "f"


class WebDriverManager:
    """Class for managing WebDriver."""

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
        chrome_options.add_argument(f'--user-agent={fake_useragent.UserAgent().random}')
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        return self.driver


# Class for playing music using WebDriver
class MusicPlayer(WebDriverManager):
    """AI is creating summary for MusicPlayer

    Args:
        WebDriverManager ([type]): [description]
    """
    # Open the search page with the given query
    def open_search_page(self, query):
        """AI is creating summary for open_search_page

        Args:
            query ([type]): [description]
        """
        self.driver.get(Config.MUSIC_SEARCH_URL.format(query=query))
        time.sleep(3)

    # Find and click the play button
    def click_play_button(self):
        """AI is creating summary for click_play_button
        """
        play_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, Config.MUSIC_PLAY_BUTTON_CLASS))
        )
        if play_button.is_enabled():
            play_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, Config.MUSIC_PLAYER_STATE_PLAYING_CLASS))
        )

    def wait_for_track_to_end(self):
        """AI is creating summary for wait_for_track_to_end
        """
        # Wait until the track finishes playing
        while True:
            player = self.driver.find_element(By.CLASS_NAME, Config.PLAYER_AUDIO_CLASS)
            player_class = player.get_attribute("class")
            if Config.MUSIC_PLAYER_STATE_PLAYING_CLASS not in player_class:
                break
            time.sleep(1)

    def play_music(self, query):
        """AI is creating summary for play_music

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            # Initialize WebDriver only when calling the method
            self.driver = self.setup_driver()
            self.open_search_page(query)
            if "404" in self.driver.title:
                return "Ошибка 404: страница не найдена!"
            self.click_play_button()
            track_name_element = self.driver.find_element(By.CLASS_NAME, Config.TRACK_INFO_CLASS)
            artist_name_element = self.driver.find_element(By.CLASS_NAME, Config.ARTIST_INFO_CLASS)
            track_name = track_name_element.text.strip()
            artist_name = artist_name_element.text.strip()
            print(f"Музыка начала играть: {artist_name} - {track_name}")
            self.wait_for_track_to_end()
            return f"Трек {artist_name} - {track_name} завершился."
        except Exception as e:
            return f"Ошибка при воспроизведении музыки: {e}"
        finally:
            if self.driver:
                self.driver.quit()

    # Request to play music
    def play_music_request(self, query):
        """AI is creating summary for play_music_request

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.play_music(query)


# Class for playing film using WebDriver
class FilmPlayer(WebDriverManager):
    """AI is creating summary for FilmPlayer

    Args:
        WebDriverManager ([type]): [description]
    """

    def __init__(self):
        super().__init__()

    # Opening of the Kinopoisk website
    def open_kinopoisk(self):
        """AI is creating summary for open_kinopoisk
        """
        self.driver.get(Config.KINOPOISK_URL)
        time.sleep(5)
        # Check if captcha appears
        try:
            captcha_checkbox = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, Config.KINOPOISK_CAPTCHA_XPATH)))
            captcha_checkbox.click()
            print("Капча обнаружена, клик выполнен")
            time.sleep(2)
        except Exception:
            print("Капча не обнаружена, продолжаем работу")

    # Search for a movie by name
    def search_film(self, film_name):
        """AI is creating summary for search_film

        Args:
            film_name ([type]): [description]
        """
        film_input = self.driver.find_element(By.XPATH, Config.KINOPOISK_SEARCH_INPUT_XPATH)
        film_input.clear()
        film_input.send_keys(film_name)
        film_input.send_keys(Keys.ENTER)
        time.sleep(5)

    # Selecting the first movie from the list
    def select_first_film(self):
        """AI is creating summary for select_first_film

        Returns:
            [type]: [description]
        """
        find_film = self.driver.find_element(By.XPATH, Config.FIRST_FILM_XPATH)
        name_film = find_film.get_attribute('textContent')
        find_film.click()
        time.sleep(5)
        return name_film

    # Going to the website sspoisk.ru
    def switch_to_sspoisk(self):
        """AI is creating summary for switch_to_sspoisk
        """
        film_url = self.driver.current_url
        new_url = film_url.replace(Config.SSPOISK_URL_REPLACE[0], Config.SSPOISK_URL_REPLACE[1])
        self.driver.get(new_url)
        time.sleep(5)

    # Switching to an iframe
    def switch_to_iframe(self):
        """AI is creating summary for switch_to_iframe
        """
        iframes = self.driver.find_elements(By.TAG_NAME, Config.IFRAME_TAG)
        if iframes:
            self.driver.switch_to.frame(iframes[0])

    # Pressing the play button
    def click_play_button(self):
        """AI is creating summary for click_play_button
        """
        play_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, Config.PLAY_BUTTON_FILM_CLASS))
        )
        if play_button.is_enabled():
            play_button.click()

    # Switching to full-screen mode
    def click_fullscreen_button(self):
        """AI is creating summary for click_fullscreen_button
        """
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Config.FULLSCREEN_BUTTON_ACTION)
        time.sleep(2)

    # Waiting for playback to start
    def wait_for_playback_to_start(self):
        """AI is creating summary for wait_for_playback_to_start
        """
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        time.sleep(2)

    # Waiting for playback to finish
    def wait_for_playback_to_end(self):
        """AI is creating summary for wait_for_playback_to_end
        """
        while True:
            play_button = self.driver.find_element(By.CLASS_NAME, Config.PLAY_BUTTON_FILM_CLASS)
            play_button_class = play_button.get_attribute("class")
            if Config.PLAY_BUTTON_PRESSED_CLASS not in play_button_class:
                break
            time.sleep(1)

    # The main method for playing a movie
    def play_film(self, film_name):
        """AI is creating summary for play_film

        Args:
            film_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            self.setup_driver()
            self.open_kinopoisk()
            self.search_film(film_name)
            name_film = self.select_first_film()
            self.switch_to_sspoisk()
            self.switch_to_iframe()
            self.click_play_button()
            self.wait_for_playback_to_start()
            self.click_fullscreen_button()
            self.wait_for_playback_to_end()
            return f"Фильм '{name_film}' завершился."
        except Exception as e:
            return f"Произошла ошибка: {e}"
        finally:
            if self.driver:
                self.driver.quit()

    # Request to play a film
    def play_film_request(self, query):
        """AI is creating summary for play_film_request

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.play_film(query)


class NetworkActions:
    """AI is creating summary for
    """
    def __init__(self):
        self.music_player = MusicPlayer()
        self.film_player = FilmPlayer()

    # Perform a web search
    def web_search(self, query):
        """AI is creating summary for web_search

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        if query:
            wb.open("https://www.google.ru/search?q=" + query)
            return "Ищу информацию по запросу " + query
        else:
            return "Я не поняла, что надо искать."

    # Check if the query is for searching
    def check_searching(self, query):
        """AI is creating summary for check_searching

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        if any(word in query for word in ["найди", "найти"]):
            query = query.replace("найди", "").replace("найти", "").strip()
            return self.web_search(query)
        else:
            return False

    # Get the weather for a given city
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

    # Opens specified URL in browser
    def open_url(self, url):
        """AI is creating summary for open_url

        Args:
            url ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            wb.open(url)
            return f"Открываю сайт: {url}"
        except Exception as e:
            return f"Ошибка при открытии сайта: {e}"
