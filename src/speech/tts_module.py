import logging
import sounddevice as sd

from piper import PiperVoice
from piper.config import SynthesisConfig

logger = logging.getLogger(__name__)


# Text-to-Speech module
class TTS:
    def __init__(self):
        model_path = "ru_RU-irina-medium.onnx"

        logger.info("Loading Piper TTS model: %s", model_path)

        self.voice = PiperVoice.load(model_path)

        self.syn_config = SynthesisConfig(
            volume=1.0,
            length_scale=1.0,
        )

    def speak(self, message):
        message_str = str(message)

        if not message_str.strip():
            return

        logger.info("Speaking: %s", message_str)

        try:
            for chunk in self.voice.synthesize(
                message_str,
                syn_config=self.syn_config
            ):
                sd.play(
                    chunk.audio_int16_array,
                    samplerate=chunk.sample_rate
                )
                sd.wait()

        except Exception as e:
            logger.exception("Piper TTS error %s", e)
