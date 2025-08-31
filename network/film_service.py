'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 31/08/2025
Ending //
'''
# Installing the necessary libraries
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from network.web_driver_manager import WebDriverManager

logger = logging.getLogger(__name__)


class FilmConfig:
    """AI is creating summary for
    """
    # Settings for Music Player
    KINOPOISK_URL = "https://www.kinopoisk.ru/"
    SSPOISK_URL_REPLACE = ("kinopoisk.ru", "sspoisk.ru")
    CAPTCHA_XPATH = '//*[@id="checkbox-captcha-form"]/div[3]/div/div[1]/div[1]'
    SEARCH_INPUT_XPATH = '//*[@id="__next"]/div[1]/div[1]/header/div/div[2]/div[2]/div/form/div/input'
    FIRST_FILM_XPATH = '//div[@class="element most_wanted"]//p[@class="name"]/a'
    IFRAME_TAG = "iframe"
    PLAY_BUTTON_CLASS = "allplay__controls__item.allplay__control"
    PLAY_BUTTON_PRESSED_CLASS = "allplay__control--pressed"
    FULLSCREEN_BUTTON_ACTION = "f"


# Handles film search operations
class FilmSearchEngine:
    """AI is creating summary for
    """

    def __init__(self, driver):
        self.driver = driver

    # Open Kinopoisk website
    def open_kinopoisk(self):
        """AI is creating summary for open_kinopoisk
        """
        self.driver.get(FilmConfig.KINOPOISK_URL)
        time.sleep(5)
        # Handle captcha if present
        try:
            captcha_checkbox = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, FilmConfig.CAPTCHA_XPATH)))
            captcha_checkbox.click()
            logger.info("Капча обнаружена, клик выполнен")
            time.sleep(2)
        except Exception:
            logger.info("Капча не обнаружена, продолжаем работу")

    # Search for film by name
    def search_film(self, film_name):
        """AI is creating summary for search_film

        Args:
            film_name ([type]): [description]
        """
        film_input = self.driver.find_element(By.XPATH, FilmConfig.SEARCH_INPUT_XPATH)
        film_input.clear()
        film_input.send_keys(film_name)
        film_input.send_keys(Keys.ENTER)
        time.sleep(5)

    def select_first_film(self):
        """Select first film from search results"""
        find_film = self.driver.find_element(By.XPATH, FilmConfig.FIRST_FILM_XPATH)
        name_film = find_film.get_attribute('textContent')
        find_film.click()
        time.sleep(5)
        return name_film

    # Switch to sspoisk website
    def switch_to_sspoisk(self):
        """AI is creating summary for switch_to_sspoisk
        """
        film_url = self.driver.current_url
        new_url = film_url.replace(
            FilmConfig.SSPOISK_URL_REPLACE[0],
            FilmConfig.SSPOISK_URL_REPLACE[1]
        )
        self.driver.get(new_url)
        time.sleep(5)


# Handles film playback operations
class FilmPlaybackEngine:
    """AI is creating summary for
    """
    def __init__(self, driver):
        self.driver = driver

    # Switch to iframe for video playback
    def switch_to_iframe(self):
        """AI is creating summary for switch_to_iframe
        """
        iframes = self.driver.find_elements(By.TAG_NAME, FilmConfig.IFRAME_TAG)
        if iframes:
            self.driver.switch_to.frame(iframes[0])

    # Start film playback
    def play(self):
        """AI is creating summary for play
        """
        play_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, FilmConfig.PLAY_BUTTON_CLASS))
        )
        if play_button.is_enabled():
            play_button.click()

    # Enter fullscreen mode
    def enter_fullscreen(self):
        """AI is creating summary for enter_fullscreen
        """
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(FilmConfig.FULLSCREEN_BUTTON_ACTION)
        time.sleep(2)

    # Start playback
    def start_playback(self):
        """AI is creating summary for start_playback
        """
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        time.sleep(2)

    # Wait until film finishes playing
    def wait_for_completion(self):
        """AI is creating summary for wait_for_completion
        """
        while True:
            play_button = self.driver.find_element(By.CLASS_NAME, FilmConfig.PLAY_BUTTON_CLASS)
            play_button_class = play_button.get_attribute("class")
            if FilmConfig.PLAY_BUTTON_PRESSED_CLASS not in play_button_class:
                break
            time.sleep(1)


# Orchestrates film-related operations
class FilmManager(WebDriverManager):
    """AI is creating summary for FilmManager

    Args:
        WebDriverManager ([type]): [description]
    """
    def __init__(self):
        super().__init__()
        self.driver = None
        self.search_engine = None
        self.music_player_engine = None
        self.video_player_engine = None

    # The main method to play film
    def play_film(self, film_name):
        """AI is creating summary for play_film

        Args:
            film_name ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            self.driver = self.setup_driver()
            # Initialize components
            self.search_engine = FilmSearchEngine(self.driver)
            self.video_player_engine = FilmPlaybackEngine(self.driver)
            # Execute film playback flow
            self.search_engine.open_kinopoisk()
            self.search_engine.search_film(film_name)
            film_title = self.search_engine.select_first_film()
            self.search_engine.switch_to_sspoisk()
            self.video_player_engine.switch_to_iframe()
            self.video_player_engine.play()
            self.video_player_engine.start_playback()
            self.video_player_engine.wait_for_completion()
            return f"Фильм '{film_title}' завершился."
        except Exception as e:
            return f"Произошла ошибка: %s" % e
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
