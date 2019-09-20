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
    assert result[0].id == "time/suggestion/number_one"
    assert result[1].id == "place/suggestion/number_one"
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
    assert utterances[0].id == "time/suggestion/sub_module/another_module/number_one"
    assert utterances[1].id == "time/suggestion/sub_module/another_module/number_two"
    assert utterances[2].id == "time/suggestion/sub_module/another_module/number_three"




def test_if_conversion_from_dict_data_to_utterance_object_works_well():
    db = UtteranceDB(DB_FILE)
    utterance = db.transform("time/suggestions/number_one", {"body": "Hey this is me", "expects_response": True})

    assert isinstance(utterance, Utterance)
    assert utterance.id == "time/suggestions/number_one"
    assert utterance.get_body() == "Hey this is me"
    assert utterance.expects_response() is True


def test_if_conversion_works_if_no_expects_response_is_set():
    db = UtteranceDB(DB_FILE)


    utterance = db.transform("hello_1", {"body": "Hey this is me"})
    assert isinstance(utterance, Utterance)
    assert utterance.id == "hello_1"
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


    utterance = db.get("time/suggestion/sub_module/another_module/number_one")

    assert isinstance(utterance, Utterance)
    assert utterance.id == "time/suggestion/sub_module/another_module/number_one"
    assert utterance.get_body() == "this is my time suggestion one"


def test_db_get_accepts_fill_ins():
    db = get_udb()
    utterance = db.get("standard/number_one", ["robert"])
    assert utterance.fill_ins[0] == "robert"


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

    random_utterance = db.get("time/suggestion/sub_module/another_module")
    assert isinstance(random_utterance, Utterance)





def test_if_db_can_parse_uid_and_a_list_of_options_from_the_agent_message_body():
    message_body = "[time/suggestion/option_1, [6pm, 7:30pm]]"

    db = UtteranceDB(DB_FILE)
    db.setup()

    uid, fill_ins = db.extract_data_from_agent_message_string(message_body)

    assert len(fill_ins) == 2
    assert uid == "time/suggestion/option_1"
    assert fill_ins[0] == "6pm"
    assert fill_ins[1] == "7:30pm"


def test_message_parser_can_deal_with_empty_list():
    message_body = "[time_suggestion_based_on_home_arrival_1, []]"

    db = UtteranceDB(DB_FILE)
    db.setup()

    uid, fill_ins = db.extract_data_from_agent_message_string(message_body)

    assert len(fill_ins) == 0
    assert type(fill_ins) == list
    assert uid == "time_suggestion_based_on_home_arrival_1"


def test_get_by_agent_string_returns_utterance_instance_when_getting_a_well_formed_string():
    message_body = "[time/suggestion/default, []]"

    db = UtteranceDB(DB_FILE)
    db.setup()

    utterance = db.get_by_agent_string(message_body)

    assert isinstance(utterance, Utterance)
    assert utterance.fill_ins == []
    assert utterance.id == "time/suggestion/default"


def test_udb_raises_excpetion_if_no_utterance_was_found():

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


    with pytest.raises(UtteranceNotFoundException):
        utterance = db.get("this/is/missing")


def test_udb_has_a_history():
    db = get_udb()
    assert hasattr(db, "history")
    assert isinstance(db.history, ConversationHistory)


def test_udb_stores_utterance_in_history_when_getting():
    db = get_udb()

    utterance = db.get("time/suggestion/sub_module/another_module/number_one")

    assert isinstance(db.history.get_last_utterance(), Utterance)
    assert db.history.get_last_utterance().id == "time/suggestion/sub_module/another_module/number_one"


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
                "body": "this is a sample"
            }
        }
    }
    db.db = db.process_modules()
    return db

