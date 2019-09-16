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


    # def run(self, queue_in: Queue, queue_out: Queue):
    def run(self):
        while True:
            # self.output.synthesizer.iterate()
            incoming = self.queue_in.get()
            if incoming:
                log.debug(f"got incoming request {incoming}")
                self.chat(incoming)


    def setup_thread(self):
        log.debug("setting up thread")
        self.thread = Thread(target=self.run, name="ioc-thread", args=(self.queue_in, self.queue_out), daemon=True)
        self.thread.start()
        log.debug("thread started")



    def setup_input(self):
        self.input = Input()

    def setup_output(self):
        self.output = Output(self.input)

    def setup_queues(self):
        self.queue_in = Queue(maxsize=0)
        self.queue_in.identifier = "this-is-queue-in"
        self.queue_out = Queue(maxsize=0)
        self.queue_out.identifier = "this-is-queue-out"

    def chat(self, utterance_id):
        # todo get utterance, pass it to output.speak
        # ava sends .send request to usercont, usercont uses IOC to talk to user and get response, response is passed back, useragent creates an achievement goal to send a message to ava with the result
        self.output.speak(Utterance("Hello, how are you?", utterance_id))

    def done(self):
        self.queue_in.taskDone()
        self.queue_out.taskDone()
        """code for cleaning up queues and threads"""
        pass



