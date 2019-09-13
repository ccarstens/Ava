

from ava.environment import Environment
from ava.ava import Ava
import time
import asyncio
import logging

# env = Environment("a@localhost", "controller_a@localhost")
# env.setup()

if __name__ == '__main__':
    ava = Ava("ava@localhost", "ava", "../asl/ava.asl")
    f = ava.start()
    f.result()
    time.sleep(3)
    ava.bdi.add_achievement_goal("testgoal")
    print(ava.bdi.get_beliefs())
    while True:
        try:
            time.sleep(0.01)
        except KeyboardInterrupt:
            ava.stop()
            break

