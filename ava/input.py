import speech_recognition as sr
from log import log_input as log
import time
from queue import Queue


class Input:
    def __init__(self):
        log.debug("init")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.queue = Queue(maxsize=0)
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen(self):
        while self.microphone.stream is not None:
            log.error("microphone is not ready")
            time.sleep(0.1)

        stop_listening = self.recognizer.listen_in_background(self.microphone, self.on_received_audio_input)

        while True:
            try:
                parsed_user_input = self.queue.get()
                if parsed_user_input:
                    log.debug(f"received parsed user input {parsed_user_input}")
                    stop_listening(wait_for_stop=False)
            except KeyboardInterrupt:
                log.debug("keyboard interrupt while waiting for microphone input")
                break

    def on_received_audio_input(self, recognizer: sr.Recognizer, audio: sr.AudioData):
        log.debug("received audio data from microphone")

