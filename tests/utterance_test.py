from ava.utterance import Utterance
from ava.exceptions import *
import pytest
from agentspeak import Literal

def test_utterance_can_replace_placeholders_in_body_with_fill_ins():
    utterance = Utterance("blank {}", "default")
    utterance.set_fill_ins(["hello"])

    body = utterance.get_body()
    assert body == "blank hello"


def test_utterance_can_deal_with_empty_fill_in_list():
    utterance = Utterance("blank", "default")

    body = utterance.get_body()
    assert body == "blank"


def test_utterance_raises_if_placeholder_in_string_but_no_fill_ins():
    utterance = Utterance("blank {}", "default")


    with pytest.raises(MissingFillInsExceptions):
        body = utterance.get_body()


def test_expects_response_method_returns_correct_value():
    utterance = Utterance("blank {}", "default", expected_reactions=["default"])

    assert utterance.expects_response()


def test_utterance_can_generate_a_statement_finished_belief():
    utterance = Utterance("blank {}", "default")

    statement_finished_belief = utterance.to_statement_finished_belief()

    assert isinstance(statement_finished_belief, Literal)
    assert statement_finished_belief.functor == "statement_finished"
    assert len(statement_finished_belief.args) == 2
    assert statement_finished_belief.args[0] == "default"
    assert isinstance(statement_finished_belief.args[1], Literal)
    assert statement_finished_belief.args[1].functor == "yes"


def test_utterance_throws_error_if_expects_response_and_statement_finished_goal_is_generated():
    utterance = Utterance("blank {}", "default", expected_reactions=["default"])

    with pytest.raises(UtteranceExpectsResponseException):
        statement_finished_belief = utterance.to_statement_finished_belief()



def test_u_has_no_public_fill_ins_property():
    utterance = Utterance("blank {}", "default")
    assert not hasattr(utterance, "fill_ins")


def test_u_can_take_an_eliciting_intention_as_an_optional_parameter():
    utterance = Utterance("blank {}", "default", expected_reactions=["confirmation"], eliciting_intention="get_time_from_user")

    assert hasattr(utterance, "eliciting_intention")
    assert utterance.eliciting_intention == "get_time_from_user"

