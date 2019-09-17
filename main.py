

from ava.environment import Environment
from ava.avaagent import AvaAgent
import time
import asyncio
import logging


if __name__ == '__main__':
    env = Environment("a@localhost", "controller_a@localhost")
    env.setup()
    env.run_once()
    x = 0
    while True:
        try:
            if x % 200 == 0:
                # print("main running")
                pass

            if x == 200:
                y = env.ava.bdi.get_beliefs()
                print(y)
                
            time.sleep(0.01)
            x += 1
        except KeyboardInterrupt:
            env.stop()
            break

