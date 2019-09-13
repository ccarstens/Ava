from log import log_iocontroller as log
from ava.output import Output

class IOController:
    def __init__(self):
        log.debug("IOController init")
        self.input = None
        self.output = None

    def setup_input(self):
        pass

    def setup_output(self):
        self.output = Output()

