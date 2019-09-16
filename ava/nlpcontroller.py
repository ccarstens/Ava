from log import log_nlp as log
from ava.directive import Directive


class NLPController:
    def __init__(self):
        log.debug("init nlpc")

    def process(self, wit_data):
        utterance_id, wit_response = wit_data


        # print("\n\n")
        # print(wit_response['entities'])
        # print("\n\n")
        # print(wit_response['entities']['intent'])
        # print("\n\n")
        # print(wit_response['entities']['intent'][0])
        # print("\n\n")
        # print(wit_response['entities']['intent'][0]['value'])


        if wit_response['entities']['intent'][0]['value']:
            intent = wit_response['entities']['intent'][0]['value']
            return Directive(utterance_id, intent)
