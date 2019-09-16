from log import log_udb as log
import json

class UtteranceDB:
    def __init__(self, db_file_path):
        log.debug("init")
        self.db_path = db_file_path
        self.db = UtteranceDB.load_db_file(db_file_path)
        pass


    @staticmethod
    def load_db_file(file_path):
        with open(file_path) as file:
            return json.load(file)

