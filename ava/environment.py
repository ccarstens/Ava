import logging
from datetime import datetime
from definitions import *
import time


class Environment:
    def __init__(self):
        self.log = None
        self.setup_logger()
        self.log.debug("ava started")

    def setup(self):
        self.log.debug("setting up environment")


    def stop(self):
        self.log.debug("stopping environment")








    def setup_logger(self):
        logging.getLogger().setLevel(logging.DEBUG)

        env_logger = logging.getLogger(__name__)
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(LOG_DIR + f"/{datetime.now(tz=None)}.log")
        # c_handler.setLevel(logging.DEBUG)
        # f_handler.setLevel(logging.DEBUG)

        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        env_logger.addHandler(c_handler)
        env_logger.addHandler(f_handler)
        self.log = env_logger
