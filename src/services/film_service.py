import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.services.web_driver_manager import WebDriverManager

logger = logging.getLogger(__name__)


class FilmConfig:
    FILM_SERVICE_URL = "https://w1.zona.im/"
    CAPTCHA_XPATH = '//*[@id="checkbox-captcha-form"]/div[3]/div/div[1]/div[1]'
    SEARCH_INPUT_XPATH = "//*[@name='search-input']"
    FIRST_FILM_XPATH = "(//div[contains(@class, 'grid')]//a[@title])[1]"
    IFRAME_TAG = "iframe"
    PLAY_BUTTON_CLASS = "vjs-big-play-button"
    PLAY_BUTTON_PRESSED_CLASS = "vjs-playing"
    FULLSCREEN_BUTTON_CLASS = "vjs-fullscreen-control"


class FilmSearchEngine:
    def __init__(self, driver):
        self.driver = driver

    # Open film service website
    def open_film_service(self):
        self.driver.get(FilmConfig.FILM_SERVICE_URL)
        time.sleep(5)
        try:
            captcha_checkbox = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, FilmConfig.CAPTCHA_XPATH)))
            captcha_checkbox.click()
            logger.info("Капча обнаружена, клик выполнен")
            time.sleep(2)
        except Exception:
            logger.info("Капча не обнаружена, продолжаем работу")

    # Search for a film by name
    def search_film(self, film_name):
        film_input = self.driver.find_element(By.XPATH, FilmConfig.SEARCH_INPUT_XPATH)
        film_input.clear()
        film_input.send_keys(film_name)
        film_input.send_keys(Keys.ENTER)
        time.sleep(5)

    # Select the first film from search results
    def select_first_film(self):
        find_film = self.driver.find_element(By.XPATH, FilmConfig.FIRST_FILM_XPATH)
        name_film = find_film.get_attribute('title')
        find_film.click()
        time.sleep(5)
        return name_film


class FilmPlaybackEngine:
    def __init__(self, driver):
        self.driver = driver

    # Switch to the video iframe
    def switch_to_iframe(self):
        iframes = self.driver.find_elements(By.TAG_NAME, FilmConfig.IFRAME_TAG)
        if iframes:
            self.driver.switch_to.frame(iframes[0])

    # Start film playback
    def play(self):
        play_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, FilmConfig.PLAY_BUTTON_CLASS))
        )
        if play_button.is_enabled():
            play_button.click()

    # Enter fullscreen mode
    def enter_fullscreen(self):
        fullscreen_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, FilmConfig.FULLSCREEN_BUTTON_CLASS))
        )
        fullscreen_button.click()

    # Start playback using the space bar
    def start_playback(self):
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        time.sleep(2)

    # Wait for film playback to finish
    def wait_for_completion(self):
        while True:
            try:
                play_button = self.driver.find_element(By.CLASS_NAME, "video-js")
                play_button_class = play_button.get_attribute("class")
                if FilmConfig.PLAY_BUTTON_PRESSED_CLASS not in play_button_class:
                    break
            except Exception:
                break
            time.sleep(1)


class FilmManager(WebDriverManager):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.search_engine = None
        self.video_player_engine = None

    # Play a film
    def play_film(self, film_name):
        try:
            self.driver = self.setup_driver()
            self.search_engine = FilmSearchEngine(self.driver)
            self.video_player_engine = FilmPlaybackEngine(self.driver)
            self.search_engine.open_film_service()
            self.search_engine.search_film(film_name)
            film_title = self.search_engine.select_first_film()
            self.video_player_engine.switch_to_iframe()
            self.video_player_engine.play()
            self.video_player_engine.start_playback()
            self.video_player_engine.enter_fullscreen()
            self.video_player_engine.wait_for_completion()
            return f"Фильм '{film_title}' завершился."
        except Exception as e:
            return f"Произошла ошибка: %s" % e
        finally:
            if self.driver:
                self.driver.quit()

    # Handle a film playback request
    def play_film_request(self, query):
        return self.play_film(query)
