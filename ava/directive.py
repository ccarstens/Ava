from agentspeak import Literal
from definitions import *

class Directive:
    def __init__(self, eliciting_utterance_id, eliciting_intention=None, intents=None):
        self.utterance_id = eliciting_utterance_id
        self.eliciting_intention = eliciting_intention

        self.intents = intents if isinstance(intents, list) else [intents]
        self.entities = []
        self.raw_wit_data = {}

    def has_intents(self):
        return len(self.intents) > 1 or self.intents[0] != NO_INTENT_DETECTED

    def add_entity(self, label, value):
        self.entities.append((label, value))

    def entity_to_literal(self, entity: tuple):
        return Literal(entity[0]), entity[1]

    def to_response_belief(self):
        entities = tuple([self.entity_to_literal(entity) for entity in self.entities])

        intent_literal = Literal(self.intents[0])

        eliciting_intention_literal = Literal(self.eliciting_intention)

        arguments = (eliciting_intention_literal, intent_literal, entities)

        return Literal("response", arguments)
