from ava.utterancedb import UtteranceDB
from ava.utterance import Utterance
from env import UTTERANCE_DB_FILE


def test_if_the_db_can_load_the_json_file():
    db = UtteranceDB(UTTERANCE_DB_FILE)

    data = db.load_db_file()


    assert isinstance(db, UtteranceDB)
    assert isinstance(data, dict)


def test_if_db_can_flatten_the_dict_from_the_json_file():
    db = UtteranceDB(UTTERANCE_DB_FILE)

    db.db_raw = db.load_db_file()

    assert db.db_raw is not None

    db.setup_flattened_db()

    assert db.db is not None
    assert len(db.db) > 0
    assert isinstance(db.db[0], Utterance)


def test_if_setup_method_loads_utterances_correctly():
    db = UtteranceDB(UTTERANCE_DB_FILE)

    db.setup()

    assert db.db_raw is not None
    assert db.db is not None
    assert len(db.db) > 0
    assert isinstance(db.db[0], Utterance)


def test_if_conversion_from_dict_data_to_utterance_object_works_well():
    db = UtteranceDB(UTTERANCE_DB_FILE)

    raw_data = ("hello_1", {"body": "Hey this is me", "expects_response": True})

    utterance = db.transform(raw_data)

    assert isinstance(utterance, Utterance)
    assert utterance.id == "hello_1"
    assert utterance.body == "Hey this is me"
    assert utterance.expects_response is True


def test_if_conversion_works_if_no_expects_response_is_set():
    db = UtteranceDB(UTTERANCE_DB_FILE)

    raw_data = ("hello_1", {"body": "Hey this is me"})

    utterance = db.transform(raw_data)
    assert isinstance(utterance, Utterance)
    assert utterance.id == "hello_1"
    assert utterance.body == "Hey this is me"
    assert utterance.expects_response is True


def test_if_db_get_returns_a_valid_utterance_instance():
    db = UtteranceDB(UTTERANCE_DB_FILE)
    db.setup()

    utterance = db.get("default")

    assert isinstance(utterance, Utterance)
    assert utterance.id == "default"


