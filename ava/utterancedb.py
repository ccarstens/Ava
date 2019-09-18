from log import log_udb as log, dump
import json
from ava.utterance import Utterance
import re


class UtteranceDB:
    def __init__(self, db_file_path):
        log.debug("init")

        self.db_raw = None
        self.db = None
        self.db_path = db_file_path

    def setup(self):
        self.db_raw = self.load_db_file()
        self.setup_flattened_db()

    def load_db_file(self):
        with open(self.db_path) as file:
            return json.load(file)

    def setup_flattened_db(self):
        if self.db_raw:
            self.db = []
            for module, utterances in self.db_raw.items():
                for utterance in utterances.items():
                    self.db.append(self.transform(utterance))

    def get(self, utterance_id):
        return next((utterance for utterance in self.db if utterance.id == utterance_id), None)

    def transform(self, utterance_data: tuple):
        id, data = utterance_data
        return Utterance(
            id=id,
            body=data["body"],
            expects_response=(data["expects_response"] if "expects_response" in data.keys() else True)
        )

    def extract_data_from_agent_message_string(self, message: str):
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
