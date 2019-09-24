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


    def get(self, domain_string, fill_ins=[]):
        matches = [utterance for utterance in self.db if domain_string in utterance.id]
        utterance = None
        if len(matches) == 1:
            utterance = matches[0]
        elif len(matches) > 1:
            utterance = random.choice(matches)

        if not utterance:
            raise UtteranceNotFoundException(domain_string)

        utterance.set_fill_ins(fill_ins)

        self.history.push(utterance)

        return utterance


    def transform(self, id, data):
        return Utterance(
            id=id,
            body=data["body"],
            expects_response=(data["expects_response"] if "expects_response" in data.keys() else True)
        )

    def extract_data_from_agent_message_string(self, message: str):
        """[time/suggestion/home_arrival_1, [6pm, 7:30pm]]"""
        uid = re.match("^\[([a-z\/_\d]+)", message)
        fillins_list_string = re.match("^\[.*\[(.*)\]\]$", message).groups(0)[0]

        def create_list_from_string(list_string):
            if "," in list_string:
                items = list_string.split(",")
            elif len(list_string.strip()):
                items = [list_string, ]
            else:
                items = []
            return [x.strip() for x in items]

        fillins_list = create_list_from_string(fillins_list_string)
        return uid.groups(0)[0], fillins_list

    def get_by_agent_string(self, message_string: str):
        utterance_id, fill_ins = self.extract_data_from_agent_message_string(message_string)
        utterance = self.get(utterance_id, fill_ins=fill_ins)
        return utterance

    def stop(self):
        log.debug("stopping db")
        self.history.serialize()
