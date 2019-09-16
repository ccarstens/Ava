from queue import Empty

from log import log_iocontroller as log
from ava.output import Output
from ava.input import Input
from ava.utterance import Utterance
from threading import Thread
from multiprocessing import Queue
import time


class IOController:
    def __init__(self, queue_in: Queue, queue_out: Queue):
        log.debug("IOController init")
        self.input = None
        self.output = None
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.thread = None
        self.setup_input()
        self.setup_output()



    def run(self):
        while True:
            try:
                incoming = self.queue_in.get_nowait()
                if incoming:
                    # todo check flag and call method that either waits for response or doesnt
                    ilf_type, utterance = incoming
                    log.debug(f"got incoming request {ilf_type}")

                    if ilf_type == 'expect_response':
                        self.chat(utterance)
                    elif ilf_type == 'statement':
                        self.statement(utterance)
                    else:
                        log.error(f"received the unknown ilf type {ilf_type}")

            except Empty:
                pass
            except KeyboardInterrupt:
                break


    def setup_input(self):
        self.input = Input(self.queue_out)

    def setup_output(self):
        self.output = Output(self.input)

    def chat(self, utterance: Utterance):
        # todo get utterance, pass it to output.speak
        # ava sends .send request to usercont, usercont uses IOC to talk to user and get response, response is passed back, useragent creates an achievement goal to send a message to ava with the result
        self.output.speak(utterance)



