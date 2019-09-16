from multiprocessing import Queue

from spade_bdi.bdi import BDIAgent
import asyncio
from log import log_user as log, dump
from spade.message import Message
from spade.template import Template
from spade_bdi.bdi import parse_literal
from spade_bdi.bdi import get_literal_from_functor_and_arguments
import aioconsole as ac
from ava.nlpcontroller import NLPController
from queue import Empty

from ava.utterance import Utterance


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

            self.agent.handle_io_response()

            await asyncio.sleep(0.005)
            # await asyncio.sleep(0.5)

        async def handle_message_with_custom_ilf_type(self, message: Message):
            functor, args = parse_literal(message.body)
            # args = args[0]

            log.debug(f"received message with custom ilf type {message}")

            utterance = Utterance("What can I do for you?", message.body)
            self.agent.io_queue_in.put(("expect_response", utterance))

    def handle_io_response(self):
        try:
            response = self.io_queue_out.get_nowait()
            if response:
                utterance_id, wit_response = response

                log.debug(f"wit response for transcript '{wit_response['_text']}' in response to utterance {utterance_id}")

                response = self.nlpc.process(response)

                log.debug(f"received directive {response.directions}")

                user_response_belief = get_literal_from_functor_and_arguments(f"responded_{response.utterance_id}", (response.directions,))

                log.debug(dump(user_response_belief))

                self.bdi.add_achievement_goal("tell_ava", user_response_belief)
        except Empty:
            pass
        pass

    def __init__(self, jid, pw, asl, io_queue_in: Queue, io_queue_out: Queue, nlpc: NLPController):
        super().__init__(jid, pw, asl)
        self.io_queue_in = io_queue_in
        self.io_queue_out = io_queue_out
        self.nlpc = nlpc
        self.active_utterance = None

    async def setup(self):
        log.debug("User agent setup")

        template = Template(metadata={"performative": "BDI"})
        personality = self.UserAgentBehaviour()
        personality.custom_ilf_types = ['getuserinput']
        self.add_behaviour(personality, template)
        personality.setup()
