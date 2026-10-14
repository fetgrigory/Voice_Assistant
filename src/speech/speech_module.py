import json
import logging
import queue
import sounddevice as sd
import vosk

logger = logging.getLogger(__name__)


class SpeechRecognizer:
    def __init__(self, model_path="vosk-model-small-ru-0.22", input_device=None):
        self.model = vosk.Model(model_path)
        self.input_device = input_device or sd.default.device[0]
        self.audio_queue = queue.Queue()

    # Listen for the activation word
    def listen_for_activation(self, activation_words, callback=None):
        samplerate = int(sd.query_devices(self.input_device, 'input')['default_samplerate'])
        rec = vosk.KaldiRecognizer(self.model, samplerate)

        def stream_callback(indata, frames, time_info, status):
            if status:
                logger.warning("Audio stream status: %s", status)
            self.audio_queue.put(bytes(indata))

        with sd.RawInputStream(
            samplerate=samplerate,
            blocksize=8000,
            device=self.input_device,
            dtype='int16',
            channels=1,
            callback=stream_callback
        ):
            logger.info("Ожидание активационного слова 'Астра'...")
            while True:
                data = self.audio_queue.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    recognized_text = result.get('text', '').lower()
                    if any(word in recognized_text for word in activation_words):
                        logger.info("Активационное слово распознано.")
                        if callback:
                            callback()
                        return

    # Recognize a voice command
    def listen_command(self, duration=5):
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