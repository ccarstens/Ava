

class Directive:
    def __init__(self, eliciting_utterance, intents=None):
        self.utterance_id = eliciting_utterance
        self.intents = intents if isinstance(intents, list) else [intents]
