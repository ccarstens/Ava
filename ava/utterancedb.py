from log import log_udb as log, dump
import json
from ava.utterance import Utterance
import re
from ava.exceptions import UtteranceModuleEmpty, UtteranceNotFoundException
import random
from ava.conversationhistory import ConversationHistory

class UtteranceDB:
    def __init__(self, db_file_path, conversation_history=ConversationHistory()):
        log.debug("init")

        self.db_raw = None
        self.db = None
        self.db_path = db_file_path
        self.history = conversation_history

    def setup(self):
        self.db_raw = self.load_db_file()
        self.db = self.process_modules()

    def load_db_file(self):
        with open(self.db_path) as file:
            return json.load(file)


    def is_module(self, module: dict):
        if len(list(module.keys())) > 0:
            return "body" not in list(module.keys())


    def process_modules(self):
        def get_domain_string(domain_string, route):
            separator = "/"
            return f"{domain_string}{separator}{route}"

        def process_layer(domain_string, module_layer: dict):
            tmp = []
            for route, module_values in module_layer.items():
                if self.is_module(module_values):
                    tmp += process_layer(get_domain_string(domain_string, route), module_values)
                else:
                    tmp.append(self.transform(get_domain_string(domain_string, route), module_values))
            return tmp
        return process_layer("", self.db_raw)


    def get(self, domain_string, fill_ins=None, eliciting_intention=None):
        if fill_ins is None:
            fill_ins = {}
        matches = [utterance for utterance in self.db if domain_string in utterance.id]
        utterance = None
        if len(matches) == 1:
            utterance = matches[0]
        elif len(matches) > 1:
            utterance = random.choice(matches)

        if not utterance:
            raise UtteranceNotFoundException(domain_string)

        utterance.set_fill_ins(fill_ins)

        utterance.eliciting_intention = eliciting_intention

        self.history.push(utterance)

        return utterance

    def get_last_utterance(self, uid=None):
        return self.history.get_last_utterance(uid=uid)

    def transform(self, id, data):
        return Utterance(
            id=id,
            body=data["body"],
            expected_reactions=(data["expected_reactions"] if "expected_reactions" in data.keys() else [])
        )

    def extract_data_from_agent_message_string(self, message: str):

        data = {}

        for functor in ["utterance_id", "eliciting_intention"]:
            data[functor] = UtteranceDB.get_argument_for_functor(functor, message)

        fillins_list_string = UtteranceDB.get_argument_for_functor("fill_ins", message, extract_list=True)

        def create_list_from_string(list_string):
            fill_in_data = {}
            list_string = list_string.strip("[]")
            if "," in list_string:
                items = list_string.split(",")
            elif len(list_string.strip()):
                items = [list_string, ]
            else:
                items = []
            for x in items:
                func, argument = UtteranceDB.get_functor_and_argument_from_literal(x.strip())
                fill_in_data[func] = argument
            return fill_in_data

        data["fill_ins"] = create_list_from_string(fillins_list_string)
        return data

    def get_by_agent_string(self, message_string: str):
        data = self.extract_data_from_agent_message_string(message_string)

        utterance = self.get(data["utterance_id"], fill_ins=data["fill_ins"])
        utterance.eliciting_intention = data["eliciting_intention"]
        return utterance

    def stop(self):
        log.debug("stopping db")
        self.history.serialize()

    @staticmethod
    def get_functor_and_argument_from_literal(literal_string: str, strip=True):
        matches = re.search(rf"^([a-zA-Z_0-1]+)\(([^()]+)\)", literal_string)

        extracted_functor = matches.group(1)
        argument = matches.group(2)

        if strip:
            argument = argument.strip('" ')

        return extracted_functor, argument


    @staticmethod
    def get_argument_for_functor(functor, literal_string, strip=True, extract_list=False):
        if extract_list and "[" in literal_string and "]" in literal_string :
            matches = re.search(rf"({functor})\(\[(.*)\]\)", literal_string)
        else:
            matches = re.search(rf"({functor})\(([^()]+)\)", literal_string)


        argument = matches.group(2)

        if strip:
            argument = argument.strip('" ')

        return argument
