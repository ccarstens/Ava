from log import log_ch as log
from ava.utterance import Utterance
from ava.directive import Directive
from env import *


class ConversationHistory:
    def __init__(self):
        log.debug("init")

        self.history = []
        self.accepted_types = [Utterance, Directive]


    def push(self, input_object):
        if type(input_object) in self.accepted_types:
            self.history.append(input_object)
        else:
            raise TypeError(f"conversation history only takes types {self.accepted_types}")


    def get_last_utterance(self, uid=None):
        return self.get_last_item_by_type(Utterance, uid=uid)

    def get_last_directive(self):
        return self.get_last_item_by_type(Directive)

    def get_last_item_by_type(self, item_type, uid=None):
        for obj in self.history[::-1]:
            if isinstance(obj, item_type) and not uid:
                return obj
            elif hasattr(obj, "id") and uid and obj.id == uid:
                return obj


    def serialize(self, file=None):
        import pickle


        if file is None:
            file = f"{GLOBAL_START_TIME}.obj"

        filehandler = open(CONVERSATION_FOLDER + file, 'wb')
        pickle.dump(self.history, filehandler)