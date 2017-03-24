import json

class MessageParser():
    def __init__(self):


        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history':self.parse_history,
        }

    def encode(self, client_input):
        request = client_input
        content = None
        for i in range(len(client_input)):
            if client_input[i] == " ":
                request = client_input[:i]
                content = client_input[i+1:]
                break


        if request in ['login','logout','msg','help','names']:
            return {'request':request, 'content':content}
        else: return None


    def parse(self, payload):
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            return '..Unknown message format..'

    def parse_error(self, payload):
        return ('error:', payload['content'])


    def parse_info(self, payload):
        return ('info:', payload['content'])

    def parse_message(self, payload):
        return (payload['sender'] + ': ', payload['content'])

    def parse_history(self, payload):
        history = ''
        for msg in payload['content']:
            history += self.parse(msg) + '\n'


