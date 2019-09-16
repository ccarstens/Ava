
class Utterance:
    def __init__(self, body, id, expects_response=True):
        self.body = body
        self.id = id
        self.expects_response = expects_response
