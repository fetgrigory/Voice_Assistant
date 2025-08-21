'''
This module make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 27/11/2024
Ending //
'''

# Installing the necessary libraries
import logging
import time
import webbrowser as wb
import fake_useragent
import feedparser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class MusicConfig:
    """AI is creating summary for
    """
    # Settings for Music Player
    SEARCH_URL = "https://rus.hitmotop.com/search?q={query}"
    PLAY_BUTTON_CLASS = "jp-play"
    PLAYER_STATE_PLAYING_CLASS = "jp-state-playing"
    PLAYER_AUDIO_CLASS = "jp-audio"
    TRACK_INFO_CLASS = "jp-track-info__track"
    ARTIST_INFO_CLASS = "jp-track-info__artist"


class FilmConfig:
    """AI is creating summary for
    """
    # Settings for Film Player
    KINOPOISK_URL = "https://www.kinopoisk.ru/"
    SSPOISK_URL_REPLACE = ("kinopoisk.ru", "sspoisk.ru")
    CAPTCHA_XPATH = '//*[@id="checkbox-captcha-form"]/div[3]/div/div[1]/div[1]'
    SEARCH_INPUT_XPATH = '//*[@id="__next"]/div[1]/div[1]/header/div/div[2]/div[2]/div/form/div/input'
    FIRST_FILM_XPATH = '//div[@class="element most_wanted"]//p[@class="name"]/a'
    IFRAME_TAG = "iframe"
    PLAY_BUTTON_CLASS = "allplay__controls__item.allplay__control"
    PLAY_BUTTON_PRESSED_CLASS = "allplay__control--pressed"
    FULLSCREEN_BUTTON_ACTION = "f"


class WebDriverManager:
    """AI is creating summary for
    """

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
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        return driver


# Handles music search operations
class MusicSearchEngine:
    """AI is creating summary for
    """
    def __init__(self, driver):
        self.driver = driver

    # Search for music by query
    def search_music(self, query):
        """AI is creating summary for search_music

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        self.driver.get(MusicConfig.SEARCH_URL.format(query=query))
        time.sleep(3)
        return "404" not in self.driver.title


# Extracts metadata from music tracks
class MusicMetadataExtractor:
    """AI is creating summary for
    """
    def __init__(self, driver):
        self.driver = driver

# Extract track metadata
    def extract_metadata(self):
        """AI is creating summary for extract_metadata

        Returns:
            [type]: [description]
        """
        try:
            track_name_element = self.driver.find_element(
                By.CLASS_NAME, MusicConfig.TRACK_INFO_CLASS)
            artist_name_element = self.driver.find_element(
                By.CLASS_NAME, MusicConfig.ARTIST_INFO_CLASS)
            return {
                'track': track_name_element.text.strip(),
                'artist': artist_name_element.text.strip()
            }
        except Exception as e:
            logger.error("Failed to extract music metadata: %s", e)
            return None


# Handles music playback operations
class MusicPlaybackEngine:
    """AI is creating summary for
    """
    def __init__(self, driver, metadata_extractor):
        self.driver = driver
        self.metadata_extractor = metadata_extractor

    # Start music playback
    def play(self):
        """AI is creating summary for play
        """
        play_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, MusicConfig.PLAY_BUTTON_CLASS))
        )
        if play_button.is_enabled():
            play_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, MusicConfig.PLAYER_STATE_PLAYING_CLASS))
        )

    # Wait until track finishes playing
    def wait_for_completion(self):
        """AI is creating summary for wait_for_completion
        """
        while True:
            player = self.driver.find_element(By.CLASS_NAME, MusicConfig.PLAYER_AUDIO_CLASS)
            player_class = player.get_attribute("class")
            if MusicConfig.PLAYER_STATE_PLAYING_CLASS not in player_class:
                break
            time.sleep(1)


# Orchestrates music-related operations
class MusicManager(WebDriverManager):
    """AI is creating summary for MusicManager

    Args:
        WebDriverManager ([type]): [description]
    """
    def __init__(self):
        super().__init__()
        self.driver = None
        self.search_engine = None
        self.metadata_extractor = None

    # Main method to play music
    def play_music(self, query):
        """AI is creating summary for play_music

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            self.driver = self.setup_driver()
            # Initialize components
            self.search_engine = MusicSearchEngine(self.driver)
            self.metadata_extractor = MusicMetadataExtractor(self.driver)
            self.music_player_engine = MusicPlaybackEngine(self.driver, self.metadata_extractor)
            # Execute music playback flow
            if not self.search_engine.search_music(query):
                return "Ошибка 404: страница не найдена!"
            self.music_player_engine.play()
            metadata = self.metadata_extractor.extract_metadata()
            if metadata:
                logger.info("Музыка начала играть: %s - %s",
                           metadata['artist'], metadata['track'])
            self.music_player_engine.wait_for_completion()
            return f"Трек {metadata['artist']} - {metadata['track']} завершился."
        except Exception as e:
            return f"Ошибка при воспроизведении музыки: %s" % e
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


# Handles weather-related operations
class WeatherService:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    # Get weather for specified city
    @staticmethod
    def get_weather(city: str) -> str:
        """AI is creating summary for get_weather

        Args:
            city (str): [description]

        Returns:
            str: [description]
        """
        try:
            url = f"http://wttr.in/{city}"
            params = {'format': 3}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response.text.strip()
            return f"Ошибка: не удалось получить данные (код {response.status_code})."
        except Exception as e:
            return f"Ошибка при получении данных о погоде: %s" % e


# Handles news-related operations
class NewsService:
    """AI is creating summary for
    """
    def __init__(self, rss_url="https://russian.rt.com/rss", news_count=5):
        self.rss_url = rss_url
        self.news_count = news_count

    @staticmethod
    # Clean HTML tags from text
    def clean_html_text(text):
        """AI is creating summary for clean_html_text

        Args:
            text ([type]): [description]

        Returns:
            [type]: [description]
        """
        if not text:
            return ""
        soup = BeautifulSoup(text, "html.parser")
        return ' '.join(soup.get_text(separator=" ", strip=True).split())

    # Fetch latest news from RSS feed
    def get_latest_news(self):
        """AI is creating summary for get_latest_news

        Returns:
            [type]: [description]
        """
        try:
            feed = feedparser.parse(self.rss_url)
            if not feed.entries:
                logger.warning("No news entries found in RSS feed")
                return None

            return [
                {
                    'title': self.clean_html_text(entry.get('title', 'Без заголовка')),
                    'summary': self.clean_html_text(
                        entry.get('summary', entry.get('description', 'Нет описания'))
                    )
                }
                for entry in feed.entries[:self.news_count]
            ]
        except Exception as e:
            logger.error("Failed to fetch news: %s", e)
            return None


# Handles web search operations
class WebSearchService:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    # Perform web search
    @staticmethod
    def web_search(query):
        if query:
            wb.open("https://www.google.ru/search?q=" + query)
            return "Ищу информацию по запросу " + query
        else:
            return "Я не поняла, что надо искать."

    def check_searching(self, query):
        """Check if query requires web search"""
        if any(word in query for word in ["найди", "найти"]):
            query = query.replace("найди", "").replace("найти", "").strip()
            return self.web_search(query)
        else:
            return False

    # Open specified URL in browser
    @staticmethod
    def open_url(url):
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
            return f"Ошибка при открытии сайта: %s" % e


# Orchestrates all network-related operations
class NetworkActions:
    """AI is creating summary for
    """
    def __init__(self):
        self.music_player = MusicManager()
        self.film_player = FilmManager()
        self.weather_service = WeatherService()
        self.news_service = NewsService()
        self.web_search_service = WebSearchService()

    # Get weather for specified city
    def get_weather(self, city):
        """AI is creating summary for get_weather

        Args:
            city ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.weather_service.get_weather(city)

    # Get latest news
    def get_latest_news(self):
        """AI is creating summary for get_latest_news

        Returns:
            [type]: [description]
        """
        return self.news_service.get_latest_news()

    # Check if query requires web search
    def check_searching(self, query):
        """AI is creating summary for check_searching

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.web_search_service.check_searching(query)

    # Open specified URL
    def open_url(self, url):
        """AI is creating summary for open_url

        Args:
            url ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.web_search_service.open_url(url)
