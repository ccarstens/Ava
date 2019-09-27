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


