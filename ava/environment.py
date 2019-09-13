import logging
from datetime import datetime
from definitions import *
import time

from log import log
from ava.avaagent import AvaAgent
from ava.useragent import UserAgent


class Environment:
    def __init__(self, agent_jid, user_controller_jid):
        log.debug("environment init")

        self.ava_jid = agent_jid
        self.user_jid = user_controller_jid

        self.ava = None
        self.user = None

    def setup(self):
        log.debug("setting up environment")
        self.setup_ava()
        self.setup_user()


    def stop(self):
        log.debug("stopping environment")
        self.ava.stop()


    def setup_ava(self):
        self.ava = AvaAgent(self.ava_jid, "ava", "../asl/ava.asl")
        future_a = self.ava.start()
        future_a.result()
        self.ava.bdi.set_singleton_belief("usercontroller", self.user_jid)

    def setup_user(self):
        self.user = UserAgent(self.user_jid, "ava", "../asl/user.asl")
        future_u = self.user.start()
        future_u.result()
        self.user.bdi.set_singleton_belief("ava", self.ava_jid)
