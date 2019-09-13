from ava.environment import Environment
import time
import logging

env = Environment()
env.setup()

while True:
    try:
        time.sleep(0.01)
    except KeyboardInterrupt:
        env.stop()
        break

