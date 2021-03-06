import logging
from definitions import *
from env import *
import pprint


LOGFILE = f"{GLOBAL_START_TIME}.log"


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
log_ioprocess = get_logger("IOPROCESS")
log_output = get_logger("OUT")
log_input = get_logger("IN")
log_nlp = get_logger("NLPC")
log_udb = get_logger("UDB")
log_ch = get_logger("CH")
