from log import log_nlp as log
from ava.directive import Directive
from ava.exceptions import *
import agentspeak as asp
from spade_bdi.bdi import get_literal_from_functor_and_arguments
from definitions import *


class NLPController:
    def __init__(self):
        log.debug("init nlpc")

    def process(self, wit_data):
        utterance, wit_response = wit_data

        intents = self.extract_intents(wit_response)
        # todo extract named entities
        directive = Directive(
            eliciting_utterance_id=utterance.id,
            eliciting_intention=utterance.eliciting_intention,
            intents=intents
        )
        directive.raw_wit_data = wit_response
        return directive

    def extract_intents(self, wit_dict):
        intent_array = NLPController.keys_exists(wit_dict, "entities", "intent")
        if not intent_array:
            return NO_INTENT_DETECTED
        else:
            return [intent["value"] for intent in intent_array]

    @staticmethod
    def extract_dinner_contact(raw: list):
        for contact in raw:
            if contact["value"] not in ["siri", "eva", "eve"]:
                return contact["value"]
        return NO_DINNER_CONTACT


    @staticmethod
    def extract_entities(raw: dict):
        if NLPController.has_entities(raw):

            data = {}
            for entity, data_list in raw["entities"].items():
                if entity != "intent":
                    data[entity] = [single["value"] for single in data_list]
            return data
        else:
            raise NoEntitiesDetected


    @staticmethod
    def has_entities(raw):
        if not NLPController.keys_exists(raw, "entities"):
            return False

        entity_keys = list(raw["entities"].keys())
        entity_keys.remove("intent")
        return len(entity_keys) > 0


    @staticmethod
    def keys_exists(element, *keys):
        '''
        Check if *keys (nested) exists in `element` (dict).
        '''
        if not isinstance(element, dict):
            raise AttributeError('keys_exists() expects dict as first argument.')
        if len(keys) == 0:
            raise AttributeError('keys_exists() expects at least two arguments, one given.')

        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return False
        return _element
