from ava.exceptions import *
from agentspeak import Literal


class Utterance:
    def __init__(self, body, id, expects_response=True):
        self._body = body
        self.id = id
        self._expects_response = expects_response
        self._fill_ins = []
        self.identifier = None

    # todo add a check whether the number of placeholders matches the number of fill ins
    def get_body(self):
        if "{}" in self._body:
            if len(self._fill_ins):
                return self._body.format(*self._fill_ins)
            else:
                raise MissingFillInsExceptions
        else:
            return self._body

    def expects_response(self):
        return self._expects_response

    def to_statement_finished_belief(self):

        if self.expects_response():
            raise UtteranceExpectsResponseException

        yes_literal = Literal("yes")
        return Literal("statement_finished", (self.id, yes_literal))

    def set_fill_ins(self, fillins: list):
        self._fill_ins = fillins

    def get_fill_ins(self, i=None):
        return self._fill_ins[i] if not i is None else self._fill_ins
