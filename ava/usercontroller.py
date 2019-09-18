from multiprocessing import Queue

from spade_bdi.bdi import BDIAgent
import asyncio
from log import log_user as log, dump
from spade.message import Message
from spade.template import Template
from spade_bdi.bdi import parse_literal
from spade_bdi.bdi import get_literal_from_functor_and_arguments
from ava.nlpcontroller import NLPController
from queue import Empty

from ava.utterancedb import UtteranceDB


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

            await asyncio.sleep(0.002)
            # await asyncio.sleep(0.5)

        async def handle_message_with_custom_ilf_type(self, message: Message):
            functor, args = parse_literal(message.body)
            # args = args[0]
            log.debug(f"received message with custom ilf type {message}")

            x = list(message.body)
            print(x)
            print(type(x))


            utterance = self.agent.db.get(message.body)

            if utterance is not None:
                self.agent.io_queue_in.put(utterance)
            else:
                log.error("no utterance received")

        # def extract_utterance_and_variable_content





    def handle_io_response(self):
        try:
            response = self.io_queue_out.get_nowait()
            if response:
                log.debug(response)
                flag, payload = response
                if flag == "STATEMENT_FINISHED":
                    log.debug("statement finished")
                    utterance = payload

                    context_literal = get_literal_from_functor_and_arguments("main")

                    status_literal = get_literal_from_functor_and_arguments("yes")


                    finished_belief = get_literal_from_functor_and_arguments("statement_finished", (utterance.id, context_literal, status_literal))


                    self.bdi.add_achievement_goal("tell_ava", finished_belief)

                    pass
                elif flag == "RECEIVED_USER_RESPONSE":
                    utterance_id, wit_response = payload
                    log.debug(f"wit response for transcript '{wit_response['_text']}' in response to utterance {utterance_id}")

                    response = self.nlpc.process(payload)

                    log.debug(f"received directive {response.directions}")

                    user_response_belief = get_literal_from_functor_and_arguments(f"responded_{response.utterance_id}", (response.directions,))

                    log.debug(dump(user_response_belief))

                    self.bdi.add_achievement_goal("tell_ava", user_response_belief)

        except Empty:
            pass
        pass

    def __init__(self, jid, pw, asl, io_queue_in: Queue, io_queue_out: Queue, nlpc: NLPController, db: UtteranceDB):
        super().__init__(jid, pw, asl)
        self.io_queue_in = io_queue_in
        self.io_queue_out = io_queue_out
        self.nlpc = nlpc
        self.db = db
        self.active_utterance = None

    async def setup(self):
        log.debug("User agent setup")

        template = Template(metadata={"performative": "BDI"})
        personality = self.UserAgentBehaviour()
        personality.custom_ilf_types = ['expect_response', 'statement']
        self.add_behaviour(personality, template)
        personality.setup()

        # message = Message(to="a@localhost")
        # message.set_metadata('performative', 'BDI')
        # message.set_metadata('ilf_type', 'tell')
        # message.body = 'test_belief("greeting_2", main, yes)'
        # await self.bdi.send(message)
