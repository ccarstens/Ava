import logging
from definitions import *
from datetime import datetime


def setup_logger():
    logging.getLogger().setLevel(logging.DEBUG)

    env_logger = logging.getLogger(__name__)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(LOG_DIR + f"/{datetime.now(tz=None)}.log")
    # c_handler.setLevel(logging.DEBUG)
    # f_handler.setLevel(logging.DEBUG)

    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    env_logger.addHandler(c_handler)
    env_logger.addHandler(f_handler)
    return env_logger



log = setup_logger()