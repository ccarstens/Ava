from ava.nlpcontroller import NLPController
from ava.directive import Directive
from definitions import *
from ava.utterance import Utterance

def test_nlpc_extracts_single_intent_from_dict():
    wit_dict = {
    '_text': 'yeah that sounds good',
    'entities': {
        'intent': [{
            'confidence': 0.82693723532401,
            'value': 'confirmation'
        }]
    },
    'msg_id': '1yoIkxVstxREydBbY'}

    nlpc = NLPController()

    intents = nlpc.extract_intents(wit_dict)

    assert isinstance(intents, list)
    assert len(intents) == 1
    assert intents[0] == "confirmation"


def test_nlpc_extracts_multiple_intents():
    wit_dict = {
    '_text': 'yeah that sounds good',
    'entities': {
        'intent': [
            {
                'confidence': 0.82693723532401,
                'value': 'confirmation'
            },
            {
                'confidence': 0.82693723532401,
                'value': 'proposal'
            }
        ]
    },
    'msg_id': '1yoIkxV8Ydx2ydBbY'}

    nlpc = NLPController()

    intents = nlpc.extract_intents(wit_dict)
    assert isinstance(intents, list)
    assert len(intents) == 2
    assert "confirmation" in intents
    assert "proposal" in intents


def test_nlpc_returns_flag_for_missing_intent():
    wit_dict = {'_text': 'that sounds good', 'entities': {}, 'msg_id': '13Wd3qwVUgMDwbTRI'}

    nlpc = NLPController()

    intents = nlpc.extract_intents(wit_dict)
    assert isinstance(intents, int)
    assert intents == NO_INTENT_DETECTED


def test_process_method_extracts_intent_correctly_from_tuple():
    wit_dict = {
    '_text': 'yeah that sounds good',
    'entities': {
        'intent': [{
            'confidence': 0.82693723532401,
            'value': 'confirmation'
        }]
    },
    'msg_id': '1yoIkxVstxREydBbY'}
    response = (Utterance("hello", "default"), wit_dict)

    nlpc = NLPController()

    directive = nlpc.process(response)

    assert isinstance(directive, Directive)
    assert len(directive.intents) == 1


def test_directive_contains_wit_data_when_created_by_nlpc():
    wit_dict = {
    '_text': 'yeah that sounds good',
    'entities': {
        'intent': [{
            'confidence': 0.82693723532401,
            'value': 'confirmation'
        }]
    },
    'msg_id': '1yoIkxVstxREydBbY'}
    response = (Utterance("hello", "default"), wit_dict)

    nlpc = NLPController()

    directive = nlpc.process(response)

    assert hasattr(directive, "raw_wit_data")
    assert directive.raw_wit_data["_text"] == "yeah that sounds good"


# def test_nlpc_extracts_all_entities_from_wit_response():
#     wit = get_query_dict()
#
#
#     entities = NLPController.extract_entities(wit)
#
#     assert "contact" in list(entities.keys())


def test_nlpc_extracts_dinner_person_from_contact_entity_raw_data():
    raw = [{
                'confidence': 0.90589,
                'suggested': True,
                'type': 'value',
                'value': 'siri'
            }, {
                'confidence': 0.91578,
                'suggested': True,
                'type': 'value',
                'value': 'lauren'
            }]

    dinner_person = NLPController.extract_dinner_contact(raw)

    assert isinstance(dinner_person, str)
    assert dinner_person == "lauren"


def get_query_dict():
    return {
        '_text': "hey siri i  want to have dinner with lauren next week can "
        'you set that up',
        'entities': {
            'contact': [{
                'confidence': 0.90589,
                'suggested': True,
                'type': 'value',
                'value': 'siri'
            }, {
                'confidence': 0.91578,
                'suggested': True,
                'type': 'value',
                'value': 'lauren'
            }],
            'datetime': [{
                'confidence': 0.9673275,
                'grain': 'week',
                'type': 'value',
                'value': '2019-09-30T00:00:00.000-07:00',
                'values': [{
                    'grain': 'week',
                    'type': 'value',
                    'value': '2019-09-30T00:00:00.000-07:00'
                }]
            }],
            'greetings': [{
                'confidence': 0.99215781699234,
                'value': 'true'
            }],
            'intent': [{
                'confidence': 0.9989392725537,
                'value': 'initial_query'
            }],
            'plan_dinner': [{
                'confidence': 1,
                'type': 'value',
                'value': 'dinner'
            }]
        },
        'msg_id': '1tu2KHjlmV2G9s1tZ'
    }