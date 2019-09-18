from ava.exceptions import *


class Utterance:
    def __init__(self, body, id, expects_response=True):
        self._body = body
        self.id = id
        self.expects_response = expects_response
        self.fill_ins = []

    def get_body(self):
        if "{}" in self._body:
            if len(self.fill_ins):
                return self._body.format(*self.fill_ins)
            else:
                raise MissingFillInsExceptions
        else:
            return self._body
