import asyncio
from log import log_ava as log
from spade.message import Message
from spade_bdi.bdi import BDIAgent
from spade.template import Template
from spade_bdi.bdi import parse_literal
from typing import Union
import agentspeak


class AvaAgent(BDIAgent):
    class AvasPersonality(BDIAgent.BDIBehaviour):
        def add_custom_actions(self):

            @self.agent.bdi_actions.add_function(".your_test", (int,))
            def _your_test(x):
                print("this is my test")
                return x

            @self.agent.bdi_actions.add_function(".ask_user", (str,))
            def _ask_user(question):
                return input(question)

            @self.agent.bdi_actions.add(".log", 1)
            def _log(agent, term, intention):
                log.debug(term.args[0])

            @self.agent.bdi_actions.add_function(".log", (str, ))
            def _log(message):
                log.debug(message)

            @self.agent.bdi_actions.add_function(".lognum", (float,))
            def _lognum(message):
                log.debug(message)

            @self.agent.bdi_actions.add_function(".modulo", (float, float))
            def _modulo(number, operand):
                return number % operand

            @self.agent.bdi_actions.add_function(".ask_user_options", (str, tuple))
            def _ask_user_options(question, options):
                readable = list(map(lambda l: str(l), options))
                response = input(question + "\n" + str(readable) + "\n: ")
                if response in readable:
                    return options[readable.index(response)]

            @self.agent.bdi_actions.add(".get_parent_intention", 1)
            def _get_parent_intention(agent, term, intention):
                calling_intention = intention.head_term.functor

                for intention_stack in agent.intentions:
                    latest_intention = intention_stack[len(intention_stack) - 1]
                    if latest_intention.head_term.functor == calling_intention:
                        parent_intention = intention_stack[len(intention_stack) - 2]
                        if agentspeak.unify(term.args[0], parent_intention.head_term, intention.scope, intention.stack):
                            yield


        async def run(self):
            await super().run()

            await asyncio.sleep(0.002)

        async def handle_message_with_custom_ilf_type(self, message: Message):
            pass

    async def setup(self):
        log.debug("Ava agent setup")
        template = Template(metadata={"performative": "BDI"})
        personality = self.AvasPersonality()
        personality.custom_ilf_types = ['expect_response', 'statement', 'tell_response']
        self.add_behaviour(personality, template)
        personality.setup()

