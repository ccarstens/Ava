

from ava.environment import Environment
from ava.avaagent import AvaAgent
import time
import asyncio
import logging


if __name__ == '__main__':
    env = Environment("a@localhost", "controller_a@localhost")
    env.setup()
    env.run_once()

    while True:
        try:
            time.sleep(0.01)
        except KeyboardInterrupt:
            env.stop()
            break

