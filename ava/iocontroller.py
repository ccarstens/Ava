from queue import Empty
from env import *
from log import log_iocontroller as log
from ava.output import Output
from ava.input import Input
from ava.utterance import Utterance
from multiprocessing import Queue
from ava.utterancedb import UtteranceDB


class IOController:
    def __init__(self, queue_in: Queue, queue_out: Queue):
        log.debug("IOController init")
        self.input = None
        self.output = None
        self.queue_in = queue_in
        self.queue_out = queue_out
        self.db = None
        self.utterance_history = []
        self.setup_db()
        self.setup_input()
        self.setup_output()



    def run(self):
        while True:
            try:
                utterance = self.queue_in.get_nowait()
                if utterance:
                    log.debug(f"got incoming request {utterance.id}")
                    self.utterance_history.append(utterance)
                    if len(utterance.get_body()):
                        self.chat(utterance)
                    else:
                        self.input.listen(utterance.id)


            except Empty:
                pass
            except KeyboardInterrupt:
                log.debug("keyboard interrupt")
                break


    def setup_input(self):
        self.input = Input(self.queue_out)

    def setup_output(self):
        self.output = Output(self.input, self.utterance_history, self.queue_out)

    def setup_db(self):
        self.db = UtteranceDB(UTTERANCE_DB_FILE)
        self.db.setup()

    def chat(self, utterance: Utterance):
        self.output.speak(utterance)

    # def history_to_id_list(self):
    #     return []
    #
    # def stop(self):




