from ava.utterance import Utterance
from ava.exceptions import *
import pytest

def test_utterance_can_replace_placeholders_in_body_with_fill_ins():
    utterance = Utterance("blank {}", "default")
    utterance.fill_ins = ["hello"]

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
