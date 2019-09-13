from ava.environment import Environment
import time
import logging

env = Environment("a@localhost", "controller_a@localhost")
env.setup()

while True:
    try:
        time.sleep(0.01)
    except KeyboardInterrupt:
        env.stop()
        break

