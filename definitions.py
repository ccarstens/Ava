import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(ROOT_DIR, 'logs')



RECEIVED_USER_RESPONSE = 1
STATEMENT_FINISHED = 2
NO_INTENT_DETECTED = 3
NO_DINNER_CONTACT = 4