'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 31/08/2025
Ending //
'''
import logging
import os
import pygame

logger = logging.getLogger(__name__)


# Sound player module
class SoundPlayer:
    """AI is creating summary for
    """
    def __init__(self):
        pygame.mixer.init()

    def play_sound(self, sound_type):
        """AI is creating summary for play_sound

        Args:
            sound_type ([type]): [description]
        """
        sound_file = f'sounds/{sound_type}.mp3'
        if os.path.exists(sound_file):
            try:
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                logger.debug("Played sound: %s", sound_file)
            except Exception as e:
                logger.error("Failed to play sound %s: %s", sound_file, e)
        else:
            logger.warning("Sound file not found: %s", sound_file)
