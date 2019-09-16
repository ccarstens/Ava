
class Utterance:
    def __init__(self, body, name, expects_response=True):
        self.body = body
        self.name = name
        self.expects_response = expects_response
