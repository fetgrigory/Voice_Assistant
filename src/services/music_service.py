import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.services.web_driver_manager import WebDriverManager

logger = logging.getLogger(__name__)


class MusicConfig:
    SEARCH_URL = "https://rus.hitmotop.com/search?q={query}"
    PLAY_BUTTON_CLASS = "jp-play"
    PLAYER_STATE_PLAYING_CLASS = "jp-state-playing"
    PLAYER_AUDIO_CLASS = "jp-audio"
    TRACK_INFO_CLASS = "jp-track-info__track"
    ARTIST_INFO_CLASS = "jp-track-info__artist"


class MusicSearchEngine:
    def __init__(self, driver):
        self.driver = driver

    # Search for music by query
    def search_music(self, query):
        self.driver.get(MusicConfig.SEARCH_URL.format(query=query))
        time.sleep(3)
        return "404" not in self.driver.title


class MusicMetadataExtractor:
    def __init__(self, driver):
        self.driver = driver

    # Extract track metadata
    def extract_metadata(self):
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


class MusicPlaybackEngine:
    def __init__(self, driver, metadata_extractor):
        self.driver = driver
        self.metadata_extractor = metadata_extractor

    # Start music playback
    def play(self):
        play_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, MusicConfig.PLAY_BUTTON_CLASS))
        )
        if play_button.is_enabled():
            play_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, MusicConfig.PLAYER_STATE_PLAYING_CLASS))
        )

    # Wait for track playback to finish
    def wait_for_completion(self):
        while True:
            player = self.driver.find_element(By.CLASS_NAME, MusicConfig.PLAYER_AUDIO_CLASS)
            player_class = player.get_attribute("class")
            if MusicConfig.PLAYER_STATE_PLAYING_CLASS not in player_class:
                break
            time.sleep(1)


class MusicManager(WebDriverManager):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.search_engine = None
        self.metadata_extractor = None
        self.music_player_engine = None

    # Play music
    def play_music(self, query):
        try:
            self.driver = self.setup_driver()
            self.search_engine = MusicSearchEngine(self.driver)
            self.metadata_extractor = MusicMetadataExtractor(self.driver)
            self.music_player_engine = MusicPlaybackEngine(self.driver, self.metadata_extractor)
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

    # Handle a music playback request
    def play_music_request(self, query):
        return self.play_music(query)
