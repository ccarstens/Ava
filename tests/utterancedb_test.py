from ava.utterancedb import UtteranceDB
from ava.utterance import Utterance
from ava.exceptions import UtteranceModuleEmpty, UtteranceNotFoundException
from ava.conversationhistory import ConversationHistory
from env import UTTERANCE_DB_FILE_TESTING as DB_FILE
import pytest


def test_if_the_db_can_load_the_json_file():
    db = UtteranceDB(DB_FILE)

    data = db.load_db_file()


    assert isinstance(db, UtteranceDB)
    assert isinstance(data, dict)


def test_contains_module_returns_true_if_dict_contains_another_module_not_utterances():
    db = UtteranceDB(DB_FILE)

    module = {"time": {
        "suggestion": {
            "number_one": {
                "body": "this is my time suggestion"
            }
        }
    }}

    assert db.is_module(module) is True
    assert db.is_module(module["time"]) is True
    assert db.is_module(module["time"]["suggestion"]) is True
    assert db.is_module(module["time"]["suggestion"]["number_one"]) is False



def test_recursive_processing():
    db = UtteranceDB(DB_FILE)
    db.db_raw = {"time": {
                "suggestion": {
                    "number_one": {
                        "body": "this is my time suggestion"
                    }
                }
            },
            "place": {
                "suggestion": {
                    "number_one": {
                        "body": "this is my place suggestion"
                    }
                }
            }}

    result = db.process_modules()

    assert isinstance(result[0], Utterance)
    assert result[0].id == "/time/suggestion/number_one"
    assert result[1].id == "/place/suggestion/number_one"
    assert result[0].get_body() == "this is my time suggestion"
    assert result[1].get_body() == "this is my place suggestion"


def test_processing_of_multiple_dimensions():
    db = UtteranceDB(DB_FILE)
    db.db_raw = {"time": {
                "suggestion": {
                    "sub_module": {
                        "another_module": {
                            "number_one": {
                                "body": "this is my time suggestion one"
                            },
                            "number_two": {
                                "body": "this is my time suggestion two"
                            },
                            "number_three": {
                                "body": "this is my time suggestion three"
                            },
                        }
                    }
                }
            }}

    utterances = db.process_modules()
    assert utterances[0].id == "/time/suggestion/sub_module/another_module/number_one"
    assert utterances[1].id == "/time/suggestion/sub_module/another_module/number_two"
    assert utterances[2].id == "/time/suggestion/sub_module/another_module/number_three"




def test_if_conversion_from_dict_data_to_utterance_object_works_well():
    db = UtteranceDB(DB_FILE)
    utterance = db.transform("/time/suggestions/number_one", {"body": "Hey this is me", "expected_reactions": ["default"]})

    assert isinstance(utterance, Utterance)
    assert utterance.id == "/time/suggestions/number_one"
    assert utterance.get_body() == "Hey this is me"
    assert utterance.expects_response() is True


def test_if_conversion_works_if_no_expects_response_is_set():
    db = UtteranceDB(DB_FILE)


    utterance = db.transform("/hello_1", {"body": "Hey this is me", "expected_reactions": ["default"]})
    assert isinstance(utterance, Utterance)
    assert utterance.id == "/hello_1"
    assert utterance.get_body() == "Hey this is me"
    assert utterance.expects_response() is True


def test_if_db_get_returns_a_valid_utterance_instance():
    db = UtteranceDB(DB_FILE)
    db.db_raw = {"time": {
        "suggestion": {
            "sub_module": {
                "another_module": {
                    "number_one": {
                        "body": "this is my time suggestion one"
                    },
                    "number_two": {
                        "body": "this is my time suggestion two"
                    },
                    "number_three": {
                        "body": "this is my time suggestion three"
                    },
                }
            }
        }
    }}
    db.db = db.process_modules()


    utterance = db.get("/time/suggestion/sub_module/another_module/number_one")

    assert isinstance(utterance, Utterance)
    assert utterance.id == "/time/suggestion/sub_module/another_module/number_one"
    assert utterance.get_body() == "this is my time suggestion one"


def test_db_get_accepts_fill_ins():
    db = get_udb()
    utterance = db.get("/standard/number_one", {"name": "robert"})
    assert utterance.get_fill_ins("name") == "robert"


def test_incomplete_domain_string_returns_random_item_from_module():
    db = UtteranceDB(DB_FILE)
    db.db_raw = {"time": {
        "suggestion": {
            "sub_module": {
                "another_module": {
                    "number_one": {
                        "body": "this is my time suggestion one"
                    },
                    "number_two": {
                        "body": "this is my time suggestion two"
                    },
                    "number_three": {
                        "body": "this is my time suggestion three"
                    },
                }
            }
        }
    }}
    db.db = db.process_modules()

    random_utterance = db.get("/time/suggestion/sub_module/another_module")
    assert isinstance(random_utterance, Utterance)


def test_udb_get_can_take_the_eliciting_intention_as_a_parameter():
    db = get_udb()

    utterance = db.get("/standard/number_one", eliciting_intention="get_time_from_user")

    assert isinstance(utterance, Utterance)
    assert utterance.eliciting_intention == "get_time_from_user"


def test_udb_can_extract_literal_functor_and_body_from_string():
    literal_string = "utterance_id(\"/time/suggestion/home_arrival_1\")"

    functor, argument = UtteranceDB.get_functor_and_argument_from_literal(literal_string)

    assert functor == "utterance_id"
    assert argument == "/time/suggestion/home_arrival_1"


def test_udb_can_extract_arguments_for_named_functor():
    literal_string = 'utterance_id("/time/suggestion/home_arrival_1"), depart_time(6:30pm), another_parameter("hello")'

    argument = UtteranceDB.get_argument_for_functor("depart_time", literal_string)

    assert argument == "6:30pm"


def test_udb_can_extract_list_content_as_argument_for_functor():
    literal_string = '[utterance_id("/time/suggestion/home_arrival_1"), eliciting_intention("my_test_intention"), fill_ins([arrival_home("6pm"), suggested_time("7:30pm")])]'

    fill_ins_string = UtteranceDB.get_argument_for_functor("fill_ins", literal_string, extract_list=True)

    assert fill_ins_string == 'arrival_home("6pm"), suggested_time("7:30pm")'


def test_if_db_can_parse_uid_and_a_list_of_options_from_the_agent_message_body():
    message_body = '[utterance_id("/time/suggestion/home_arrival_1"), eliciting_intention("my_test_intention"), fill_ins([arrival_home("6pm"), suggested_time("7:30pm")])]'

    db = get_udb()

    data = db.extract_data_from_agent_message_string(message_body)


    assert len(list(data.keys())) == 3
    assert data["utterance_id"] == "/time/suggestion/home_arrival_1"
    assert data["eliciting_intention"] == "my_test_intention"
    assert isinstance(data["fill_ins"], dict)
    assert "arrival_home" in data["fill_ins"].keys()
    assert "suggested_time" in data["fill_ins"].keys()
    assert data["fill_ins"]["arrival_home"] == "6pm"
    assert data["fill_ins"]["suggested_time"] == "7:30pm"


def test_message_parser_can_deal_with_empty_list():
    message_body = '[utterance_id("/time/suggestion/home_arrival_1"), eliciting_intention("my_test_intention"), fill_ins([])]'


    db = UtteranceDB(DB_FILE)
    db.setup()

    data = db.extract_data_from_agent_message_string(message_body)

    assert len(list(data["fill_ins"].keys())) == 0
    assert type(data["fill_ins"]) == dict
    assert data["utterance_id"] == "/time/suggestion/home_arrival_1"


def test_get_by_agent_string_returns_utterance_instance_when_getting_a_well_formed_string():
    message_body = '[utterance_id("/standard/number_one"), eliciting_intention("my_test_intention"), fill_ins([])]'

    db = get_udb()

    utterance = db.get_by_agent_string(message_body)

    assert isinstance(utterance, Utterance)
    assert utterance.get_fill_ins() == {}
    assert utterance.id == "/standard/number_one"


def test_get_by_agent_string_returns_utterance_with_existing_fill_ins():
    message_body = '[utterance_id("/standard/number_one"), eliciting_intention("my_test_intention"), fill_ins([arrival_home("6pm"), suggested_time("7:30pm")])]'

    db = get_udb()

    utterance = db.get_by_agent_string(message_body)

    assert isinstance(utterance, Utterance)
    assert utterance.get_fill_ins() == {"suggested_time": "7:30pm", "arrival_home": "6pm"}
    assert utterance.id == "/standard/number_one"


def test_udb_raises_excpetion_if_no_utterance_was_found():

    db = get_udb()

    with pytest.raises(UtteranceNotFoundException):
        utterance = db.get("/this/is/missing")


def test_udb_has_a_history():
    db = get_udb()
    assert hasattr(db, "history")
    assert isinstance(db.history, ConversationHistory)


def test_udb_stores_utterance_in_history_when_getting():
    db = get_udb()

    utterance = db.get("/time/suggestion/sub_module/another_module/number_one")

    assert isinstance(db.history.get_last_utterance(), Utterance)
    assert db.history.get_last_utterance().id == "/time/suggestion/sub_module/another_module/number_one"


def test_udb_can_get_last_utterance_form_history_with_own_method():
    db = get_udb()
    utterance = db.get("/standard/number_one")

    last_utterance = db.get_last_utterance()

    assert utterance == last_utterance


def test_udb_can_get_last_utterance_form_history_by_uid_with_own_method():
    db = get_udb()
    utterance = db.get("/standard/number_one")
    next_utterance = db.get("/time/suggestion/sub_module/another_module/number_one")

    last_utterance = db.get_last_utterance("/standard/number_one")

    assert utterance == last_utterance



def get_udb():
    db = UtteranceDB(DB_FILE)
    db.db_raw = {
        "time": {
            "suggestion": {
                "sub_module": {
                    "another_module": {
                        "number_one": {
                            "body": "this is my time suggestion one"
                        },
                        "number_two": {
                            "body": "this is my time suggestion two"
                        },
                        "number_three": {
                            "body": "this is my time suggestion three"
                        },
                    }
                }
            }
        },
        "standard": {
            "number_one": {
                "body": "this is a sample for {name}"
            }
        }
    }
    db.db = db.process_modules()
    return db

