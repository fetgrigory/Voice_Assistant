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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from network.web_driver_manager import WebDriverManager

logger = logging.getLogger(__name__)


class MusicConfig:
    """AI is creating summary for
    """
    # Settings for Film Player
    SEARCH_URL = "https://rus.hitmotop.com/search?q={query}"
    PLAY_BUTTON_CLASS = "jp-play"
    PLAYER_STATE_PLAYING_CLASS = "jp-state-playing"
    PLAYER_AUDIO_CLASS = "jp-audio"
    TRACK_INFO_CLASS = "jp-track-info__track"
    ARTIST_INFO_CLASS = "jp-track-info__artist"


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
        self.music_player_engine = None

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
