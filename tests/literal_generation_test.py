import agentspeak as asp
import agentspeak.runtime
from spade_bdi.bdi import get_literal_from_functor_and_arguments
from log import log_environment as log, dump


def test_get_literal_without_args():
    intention = asp.runtime.Intention()
    literal_with_one_argument = asp.Literal("hello")
    literal_with_one_argument = asp.freeze(literal_with_one_argument, intention.scope, {})

    assert isinstance(literal_with_one_argument, asp.Literal)


def test_bdi_method_creates_literals_without_arguments():

    literal = get_literal_from_functor_and_arguments("hello")

    assert isinstance(literal, asp.Literal)


def test_bdi_method_creates_literals_with_multiple_arguments():

    literal = get_literal_from_functor_and_arguments("hello", ("this", "is", "a", "test"))
    assert isinstance(literal, asp.Literal)


def test_response_literal():

    intents = [asp.Literal(intent) for intent in ["confirmation", "proposal"]]
    literal = get_literal_from_functor_and_arguments("responded", ("default/hello_1", intents))
    assert isinstance(literal, asp.Literal)
    pass

# def test_get_literal_from_functor



