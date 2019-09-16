from log import log_udb as log, dump
import json
from ava.utterance import Utterance


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

