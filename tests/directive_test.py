from ava.directive import *
from agentspeak import Literal

def test_directive_can_add_entities():
    directive = Directive("default", "confirmation")

    directive.add_entity("degree", 59)

    assert ("degree", 59) in directive.entities


def test_entity_to_literal_transforms_the_label_to_literal():
    directive = Directive("default", "confirmation")
    directive.add_entity("degree", 59)

    transformed = directive.entity_to_literal(directive.entities[0])

    assert isinstance(transformed, tuple)
    assert isinstance(transformed[0], Literal)


def test_to_response_belief_returns_a_belief_containing_the_uid_intent_and_all_entities():
    directive = Directive("default", "confirmation")
    directive.add_entity("degree", 59)
    directive.add_entity("centimeter", 20)

    belief_literal = directive.to_response_belief()

    assert isinstance(belief_literal, Literal)
    assert belief_literal.functor == "response"
    assert "default" in belief_literal.args
    assert belief_literal.args[1].functor == "confirmation"
    assert isinstance(belief_literal.args[2], tuple)
    assert len(belief_literal.args[2]) == 2


def test_directive_without_entities_returns_response_literal_with_empty_tuple():
    directive = Directive("default", "confirmation")
    belief_literal = directive.to_response_belief()

    assert isinstance(belief_literal, Literal)
    assert belief_literal.functor == "response"
    assert "default" in belief_literal.args
    assert belief_literal.args[1].functor == "confirmation"
    assert isinstance(belief_literal.args[2], tuple)
    assert len(belief_literal.args[2]) == 0

