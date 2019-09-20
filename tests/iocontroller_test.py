import pytest
from ava.iocontroller import IOController
from ava.utterance import Utterance
from multiprocessing import Queue


def get_controller_instance():
    return IOController(Queue(), Queue())


def test_controller_has_utterance_history():
    ioc = get_controller_instance()
    assert hasattr(ioc, "utterance_history")
    assert isinstance(ioc.utterance_history, list)