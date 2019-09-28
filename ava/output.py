import pyttsx3
from ava.utterance import Utterance
from log import log_output as log
from ava.input import Input
from ava.utterancedb import UtteranceDB
from multiprocessing import Queue
from ava.exceptions import IOCNoUtteranceNotFoundInHistory
from definitions import *

class Output:
    def __init__(self, input: Input, history: list, io_queue_out: Queue):
        self.synthesizer = pyttsx3.init(debug=True)

        self.voice = [voice for voice in self.synthesizer.getProperty('voices') if "Tracy" in voice.name][0]
        self.synthesizer.setProperty('voice', self.voice.id)
        self.synthesizer.setProperty('rate', 175)

        self.input = input
        self.utterance_history = history
        self.io_queue_out = io_queue_out

        self.setup_callbacks()


        # self.synthesizer.startLoop(useDriverLoop=False)


    def setup_callbacks(self):
        self.synthesizer.connect('finished-utterance', self.on_finished_utterance)
        self.synthesizer.connect('started-word', self.on_started_word)

    def speak(self, utterance: Utterance):
        self.synthesizer.say(utterance.get_body(), utterance.id)
        self.synthesizer.runAndWait()

    def on_finished_utterance(self, name, completed):
        log.debug(f"finished speaking utterance {name}")

        utterance = self.get_last_utterance_from_history_by_id(name)
        if utterance.expects_response():
            self.input.listen(name)
        else:
            log.debug(f"no response expected, putting {utterance.id} in the queue now")
            self.io_queue_out.put((STATEMENT_FINISHED, utterance))

    def on_started_word(self, name, location, length):
        pass

    def get_last_utterance_from_history_by_id(self, uid: str):
        for utterance in self.utterance_history[::-1]:
            if utterance.id == uid:
                return utterance

        raise IOCNoUtteranceNotFoundInHistory(uid)
