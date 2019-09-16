import logging
from definitions import *
from datetime import datetime
import pprint

LOGFILE = f"{datetime.now(tz=None)}.log"


def get_logger(classname):
    logging.getLogger().setLevel(logging.DEBUG)

    logger = logging.getLogger(classname)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(LOG_DIR + "/" + LOGFILE)
    # c_handler.setLevel(logging.DEBUG)
    # f_handler.setLevel(logging.DEBUG)

    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger


pp = pprint.PrettyPrinter(indent=4)
dump = pp.pformat



log_environment = get_logger("ENV")
log_ava = get_logger("AVA")
log_user = get_logger("USER")
log_iocontroller = get_logger("IOC")
log_output = get_logger("OUT")
log_input = get_logger("IN")
log_nlp = get_logger("NLPC")
