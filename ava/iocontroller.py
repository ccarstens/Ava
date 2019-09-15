from log import log_iocontroller as log
from ava.output import Output
from ava.input import Input
from ava.utterance import Utterance
from threading import Thread
from queue import Queue
import time


class IOController:
    def __init__(self):
        log.debug("IOController init")
        self.input = None
        self.output = None
        self.queue_in = None
        self.queue_out = None
        self.thread = None
        self.setup_queues()
        self.setup_input()
        self.setup_output()
        self.setup_thread()

    def run(self, queue_in: Queue, queue_out: Queue):
        while True:
            print(queue_in.identifier)
            incoming = queue_in.get()
            if incoming:
                log.debug(f"got incoming request {incoming}")


    def setup_thread(self):
        log.debug("setting up thread")
        self.thread = Thread(target=self.run, name="ioc-thread", args=(self.queue_in, self.queue_out), daemon=True)
        self.thread.start()
        log.debug("thread started")



    def setup_input(self):
        self.input = Input()

    def setup_output(self):
        self.output = Output()

    def setup_queues(self):
        self.queue_in = Queue(maxsize=0)
        self.queue_in.identifier = "this-is-queue-in"
        self.queue_out = Queue(maxsize=0)

    def chat(self, utterance_id):
        # todo get utterance, pass it to output.speak
        # ava sends .send request to usercont, usercont uses IOC to talk to user and get response, response is passed back, useragent creates an achievement goal to send a message to ava with the result
        log.debug(utterance_id)

    def done(self):
        self.queue_in.taskDone()
        self.queue_out.taskDone()
        """code for cleaning up queues and threads"""
        pass

