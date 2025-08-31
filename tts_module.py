'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 31/08/2025
Ending //
'''
# Installing the necessary libraries
import logging
import pyttsx3
logger = logging.getLogger(__name__)


# Text-to-Speech module
class TTS:
    """AI is creating summary for
    """
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200)
        self.engine.setProperty('volume', 1)

    def speak(self, message):
        """AI is creating summary for speak

        Args:
            message ([type]): [description]
        """
        message_str = str(message)
        logger.info("Speaking: %s", message_str)
        try:
            self.engine.say(message_str)
            self.engine.runAndWait()
        except Exception as e:
            logger.error("TTS error: %s", e)
