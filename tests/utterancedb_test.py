from ava.utterancedb import UtteranceDB
from env import UTTERANCE_DB_FILE


def test_if_the_db_can_load_the_json_file():
    db = UtteranceDB(UTTERANCE_DB_FILE)

    data = UtteranceDB.load_db_file(UTTERANCE_DB_FILE)


    assert isinstance(db, UtteranceDB)
    assert isinstance(data, dict)


