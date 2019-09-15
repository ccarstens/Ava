import pyttsx3
from ava.utterance import Utterance
from log import log_output as log
import threading


class Output:
    def __init__(self):
        self.synthesizer = pyttsx3.init(debug=True)
        self.voice = list(filter(lambda sv: ('Tracy' in sv.name),
                                 self.synthesizer.getProperty('voices')))[0]
        self.synthesizer.setProperty('voice', self.voice.id)
        self.synthesizer.setProperty('rate', 175)

        self.setup_callbacks()

        # self.synthesizer.startLoop(useDriverLoop=False)


    def setup_callbacks(self):
        self.synthesizer.connect('finished-utterance', self.on_finished_utterance)
        self.synthesizer.connect('started-word', self.on_started_word)

    def speak(self, utterance: Utterance):
        self.synthesizer.say(utterance.body, utterance.name)
        self.synthesizer.runAndWait()

    def on_finished_utterance(self, name, completed):
        log.debug(f"END {name}")

    def on_started_word(self, name, location, length):
        pass

    def killme(self, synth):
        print("killme")
        synth.endLoop()

