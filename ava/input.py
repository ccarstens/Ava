import speech_recognition as sr
from log import log_input as log
import time
from multiprocessing import Queue
from env import *


class Input:
    def __init__(self, io_queue_out: Queue):
        log.debug("init")

        self.identifier = "input-object-1"
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.queue = Queue(maxsize=0)  # inter-method queue, get wit data from callback to listen method
        self.io_queue_out = io_queue_out
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen(self):
        while self.microphone.stream is not None:
            log.error("microphone is not ready")
            time.sleep(0.1)

        stop_listening = self.recognizer.listen_in_background(self.microphone, self.on_received_audio_input)
        log.debug("microphone is ready to listen")

        while True:
            try:
                parsed_user_input = self.queue.get()
                if parsed_user_input:
                    log.debug(f"received parsed user input {parsed_user_input}")
                    self.io_queue_out.put(parsed_user_input)
                    stop_listening(wait_for_stop=False)
                    return True
            except KeyboardInterrupt:
                log.debug("keyboard interrupt while waiting for microphone input")
                break

    def on_received_audio_input(self, recognizer: sr.Recognizer, audio: sr.AudioData):
        log.debug("received audio data from microphone")
        try:
            wit_data = recognizer.recognize_wit(audio, key=WIT_API_KEY, show_all=True)
            self.queue.put(wit_data)
        except sr.UnknownValueError:
            log.exception("wit.ai could not understand audio")
        except sr.RequestError as e:
            log.exception("Could not request results from wit.ai")

