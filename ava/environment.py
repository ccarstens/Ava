import logging
from datetime import datetime
from definitions import *
import time

from log import log
from ava.ava import Ava


class Environment:
    def __init__(self, agent_jid, user_controller_jid):
        log.debug("environment init")

        self.ava_jid = agent_jid
        self.user_jid = user_controller_jid

        self.ava = None
        self.user = None

    def setup(self):
        log.debug("setting up environment")
        self.ava = Ava()



    def stop(self):
        log.debug("stopping environment")



