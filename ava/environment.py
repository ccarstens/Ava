import logging
from datetime import datetime
from env import *
import time
import asyncio
from log import log_environment as log
from ava.avaagent import AvaAgent
from ava.usercontroller import UserController
from ava.iocontroller import IOController


class Environment:
    def __init__(self, agent_jid, user_controller_jid):
        log.debug("environment init")

        self.ava_jid = agent_jid
        self.user_jid = user_controller_jid

        self.ava = None
        self.user = None
        self.io = None

    def run_once(self):
        """mostly for testing features"""
        # user_input = self.io.input.listen()
        # log.debug(f"received user input {user_input}")

    def setup(self):
        log.debug("setting up environment")
        self.setup_io()
        self.setup_ava()
        self.setup_user()

        self.ava.bdi.set_singleton_belief("started", "yes")
        self.ava.bdi.add_achievement_goal("main")


    def stop(self):
        log.debug("stopping environment")
        self.ava.stop()
        self.user.stop()
        self.stop_io()

    def setup_ava(self):
        self.ava = AvaAgent(self.ava_jid, "ava", ASL_AVA)
        future_a = self.ava.start()
        future_a.result()
        self.ava.bdi.set_singleton_belief("usercontroller", self.user_jid)

    def setup_user(self):
        self.user = UserController(self.user_jid, "ava", ASL_USER, self.io)
        future_u = self.user.start()
        future_u.result()
        self.user.bdi.set_singleton_belief("ava", self.ava_jid)

    def setup_io(self):
        self.io = IOController()

    def stop_io(self):
        pass
