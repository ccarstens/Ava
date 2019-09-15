from log import log_iocontroller as log
from ava.output import Output
from ava.input import Input
from ava.utterance import Utterance


class IOController:
    def __init__(self):
        log.debug("IOController init")
        self.input = None
        self.output = None
        self.setup_input()
        self.setup_output()

    def setup_input(self):
        self.input = Input()

    def setup_output(self):
        self.output = Output()

    def chat(self, utterance_id):
        # todo get utterance, pass it to output.speak
        # ava sends .send request to usercont, usercont uses IOC to talk to user and get response, response is passed back, useragent creates an achievement goal to send a message to ava with the result
        log.debug(utterance_id)

