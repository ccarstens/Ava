import pytest
from ava.environment import Environment
import logging


def tes_init():
    env = Environment("", "")
    assert isinstance(env.log, logging.Logger)
    assert isinstance(env, Environment)