import pyttsx3
from ava.utterance import Utterance
from log import log_output as log
from ava.input import Input
from ava.utterancedb import UtteranceDB
from multiprocessing import Queue


class Output:
    def __init__(self, input: Input, db: UtteranceDB, io_queue_out: Queue):
        self.synthesizer = pyttsx3.init(debug=True)
        self.voice = list(filter(lambda sv: ('Tracy' in sv.name),
                                 self.synthesizer.getProperty('voices')))[0]
        self.synthesizer.setProperty('voice', self.voice.id)
        self.synthesizer.setProperty('rate', 175)

        self.input = input
        self.db = db
        self.io_queue_out = io_queue_out

        self.setup_callbacks()


        # self.synthesizer.startLoop(useDriverLoop=False)


    def setup_callbacks(self):
        self.synthesizer.connect('finished-utterance', self.on_finished_utterance)
        self.synthesizer.connect('started-word', self.on_started_word)

    def speak(self, utterance: Utterance):
        self.synthesizer.say(utterance.body, utterance.id)
        self.synthesizer.runAndWait()

    def on_finished_utterance(self, name, completed):
        log.debug(f"finished speaking utterance {name}")

        utterance = self.db.get(name)
        if utterance.expects_response:
            self.input.listen(name)
        else:
            self.io_queue_out.put(("STATEMENT_FINISHED", utterance))

    def on_started_word(self, name, location, length):
        pass

    def killme(self, synth):
        print("killme")
        synth.endLoop()

