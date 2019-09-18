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
    assert utterance.get_body() == "Hey this is me"
    assert utterance.expects_response is True


def test_if_conversion_works_if_no_expects_response_is_set():
    db = UtteranceDB(UTTERANCE_DB_FILE)

    raw_data = ("hello_1", {"body": "Hey this is me"})

    utterance = db.transform(raw_data)
    assert isinstance(utterance, Utterance)
    assert utterance.id == "hello_1"
    assert utterance.get_body() == "Hey this is me"
    assert utterance.expects_response is True


def test_if_db_get_returns_a_valid_utterance_instance():
    db = UtteranceDB(UTTERANCE_DB_FILE)
    db.setup()

    utterance = db.get("default")

    assert isinstance(utterance, Utterance)
    assert utterance.id == "default"


def test_if_db_can_parse_uid_and_a_list_of_options_from_the_agent_message_body():
    message_body = "[time/suggestion/option_1, [6pm, 7:30pm]]"

    db = UtteranceDB(UTTERANCE_DB_FILE)
    db.setup()

    uid, fill_ins = db.extract_data_from_agent_message_string(message_body)

    assert len(fill_ins) == 2
    assert uid == "time/suggestion/option_1"
    assert fill_ins[0] == "6pm"
    assert fill_ins[1] == "7:30pm"


def test_message_parser_can_deal_with_empty_list():
    message_body = "[time_suggestion_based_on_home_arrival_1, []]"

    db = UtteranceDB(UTTERANCE_DB_FILE)
    db.setup()

    uid, fill_ins = db.extract_data_from_agent_message_string(message_body)

    assert len(fill_ins) == 0
    assert type(fill_ins) == list
    assert uid == "time_suggestion_based_on_home_arrival_1"


def test_get_by_agent_string_returns_utterance_instance_when_getting_a_well_formed_string():
    message_body = "[default, []]"

    db = UtteranceDB(UTTERANCE_DB_FILE)
    db.setup()

    utterance = db.get_by_agent_string(message_body)

    assert isinstance(utterance, Utterance)
    assert utterance.fill_ins == []
    assert utterance.id == "default"
