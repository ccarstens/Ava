from ava.conversationhistory import ConversationHistory
from ava.utterance import Utterance
from ava.directive import Directive
import pytest

def test_ch_has_list_representing_the_history():
    ch = ConversationHistory()

    assert hasattr(ch, "history")
    assert isinstance(ch.history, list)


def test_ch_can_store_utterances():
    u = Utterance("this is the body", "this is the id")
    ch = ConversationHistory()

    ch.push(u)

    assert ch.history[0] == u


def test_ch_only_accepts_utterance_and_directive():

    class MyClass:
        pass

    d = Directive("this/is/the/id", "confirmation")
    u = Utterance("this is the body", "this/is/the/id")
    m = MyClass()

    ch = ConversationHistory()

    ch.push(d)
    ch.push(u)


    assert ch.history[0] == d
    assert ch.history[1] == u
    with pytest.raises(TypeError):
        ch.push(m)


def test_ch_can_return_last_utterance():
    ch = ConversationHistory()
    ch.push(Utterance("body", "number/one"))
    ch.push(Directive("number/one"))

    utterance = ch.get_last_utterance()

    assert isinstance(utterance, Utterance)
    assert utterance.id == "number/one"


def test_ch_can_return_last_directive():
    ch = ConversationHistory()
    ch.push(Utterance("body", "number/one"))
    ch.push(Directive("number/one"))

    directive = ch.get_last_directive()

    assert isinstance(directive, Directive)


def test_get_last_object_by_type():
    ch = ConversationHistory()
    ch.push(Utterance("body", "number/one"))
    ch.push(Directive("number/one"))

    utterance = ch.get_last_item_by_type(Utterance)
    directive = ch.get_last_item_by_type(Directive)

    assert isinstance(utterance, Utterance)
    assert isinstance(directive, Directive)


def test_ch_can_get_last_utterance_based_on_id():
    ch = ConversationHistory()
    ch.push(Utterance("this is the first one", "number/one"))
    ch.push(Directive("number/one"))
    ch.push(Utterance("this one got repeated", "number/one"))
    ch.push(Directive("number/one"))
    ch.push(Utterance("body", "number/two"))

    utterance = ch.get_last_utterance("number/one")

    assert isinstance(utterance, Utterance)
    assert utterance.get_body() == "this one got repeated"
