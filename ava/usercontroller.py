from multiprocessing import Queue

from spade_bdi.bdi import BDIAgent
import asyncio
from log import log_user as log
from spade.message import Message
from spade.template import Template
from spade_bdi.bdi import parse_literal
import aioconsole as ac
from ava.iocontroller import IOController
from queue import Empty


class UserController(BDIAgent):
    class UserAgentBehaviour(BDIAgent.BDIBehaviour):
        def add_custom_actions(self):

            @self.agent.bdi_actions.add_function(".ask_user", (str,))
            def _ask_user(question):
                return input(question)

            @self.agent.bdi_actions.add_function(".log", (str,))
            def _log(message):
                log.info(message)

            @self.agent.bdi_actions.add_function(".ask_user_options", (str, tuple))
            def _ask_user_options(question, options):
                readable = list(map(lambda l: str(l), options))
                response = input(question + "\n" + str(readable) + "\n: ")
                if response in readable:
                    return options[readable.index(response)]

        async def run(self):
            await super().run()

            try:
                response = self.agent.io_queue_out.get_nowait()
                if response:
                    log.debug(f"YEAHHHH {response['_text']}")
            except Empty:
                pass

            # if self.agent.io_queue_out.full():
            #     log.debug("something in the queue")
            #     log.debug("YEEEEAHHHHH")

            # await asyncio.sleep(0.005)
            await asyncio.sleep(0.5)

        async def handle_message_with_custom_ilf_type(self, message: Message):
            functor, args = parse_literal(message.body)
            # args = args[0]
            log.debug(f"received message with custom ilf type {message}")
            self.agent.io_queue_in.put(message.body)
            # handle communication with user here
            # print("run: ", args[0])
            # print("run: ", args[1])

            # response = await ac.ainput("XX")
            # self.add_achievement_goal("tell_va", response, source=message.sender)

    def __init__(self, jid, pw, asl, io_queue_in: Queue, io_queue_out: Queue):
        super().__init__(jid, pw, asl)
        self.io_queue_in = io_queue_in
        self.io_queue_out = io_queue_out

    async def setup(self):
        log.debug("User agent setup")

        template = Template(metadata={"performative": "BDI"})
        personality = self.UserAgentBehaviour()
        personality.custom_ilf_types = ['getuserinput']
        self.add_behaviour(personality, template)
        personality.setup()
