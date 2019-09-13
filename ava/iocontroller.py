from log import log_iocontroller as log
from ava.output import Output
from ava.utterance import Utterance

class IOController:
    def __init__(self):
        log.debug("IOController init")
        self.input = None
        self.output = None
        self.setup_output()
        u = Utterance("Hello!", 'hello-1')
        u2 = Utterance("Hey there", 'hello-2')
        self.output.speak(u)
        self.output.speak(u2)

    def setup_input(self):
        pass

    def setup_output(self):
        self.output = Output()

