'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 31/08/2025
Ending //
'''
import json
import logging
import queue
import sounddevice as sd
import vosk

logger = logging.getLogger(__name__)


# Speech recognition module
class SpeechRecognizer:
    """AI is creating summary for
    """
    def __init__(self, model_path="vosk-model-small-ru-0.22", input_device=None):
        self.model = vosk.Model(model_path)
        self.input_device = input_device or sd.default.device[0]
        self.audio_queue = queue.Queue()

    # Constantly listens to ambient sounds while waiting for the activation word
    def listen_for_activation(self, activation_words, callback=None):
        """AI is creating summary for listen_for_activation

        Args:
            activation_words ([type]): [description]
            callback ([type], optional): [description]. Defaults to None.
        """
        samplerate = int(sd.query_devices(self.input_device, 'input')['default_samplerate'])
        rec = vosk.KaldiRecognizer(self.model, samplerate)

        def stream_callback(indata, frames, time_info, status):
            if status:
                logger.warning("Audio stream status: %s", status)
            self.audio_queue.put(bytes(indata))
            # Start recording audio in a continuous stream
        with sd.RawInputStream(
            samplerate=samplerate,
            blocksize=8000,
            device=self.input_device,
            dtype='int16',
            channels=1,
            callback=stream_callback
        ):
            # Notify that the assistant is waiting for the keyword
            logger.info("Ожидание активационного слова 'Астра'...")
            while True:
                data = self.audio_queue.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    recognized_text = result.get('text', '').lower()
                    # Check if the activation keyword 'Астра' is in the recognized text
                    if any(word in recognized_text for word in activation_words):
                        # Notify that the keyword was detected
                        logger.info("Активационное слово распознано.")
                        if callback:
                            callback()
                        return

    def listen_command(self, duration=5):
        """AI is creating summary for listen_command

        Args:
            duration (int, optional): [description]. Defaults to 5.

        Returns:
            [type]: [description]
        """
        samplerate = int(sd.query_devices(self.input_device, 'input')['default_samplerate'])
        try:
            audio = sd.rec(
                int(duration * samplerate),
                samplerate=samplerate,
                device=self.input_device,
                channels=1,
                dtype='int16'
            )
            sd.wait()

            rec = vosk.KaldiRecognizer(self.model, samplerate)
            if rec.AcceptWaveform(audio.tobytes()):
                result = json.loads(rec.Result())
                query = result.get('text', '').lower()
                logger.info("Recognized: %s", query)
                return query
            return None
        except Exception as e:
            logger.error("Audio recording error: %s", e)
            return None
