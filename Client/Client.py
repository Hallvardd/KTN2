# -*- coding: utf-8 -*-
import socket
import json
import sys
from MessageParser import MessageParser
from MessageReceiver import MessageReceiver


class Client:
    """
    This is the chat client class
    """
    host = None
    server_port = None
    parser = None

    def __init__(self, host, server_port):
        self.parser = MessageParser()
        self.host = host
        self.server_port = server_port
        """
        This method is run when creating a new Client object
        """
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.thread = MessageReceiver(self, self.connection)
        self.thread.start()
        print('Welcome, please login:')
        while True:
            user_input = input('>>')
            dict_payload = self.parser.encode(user_input)
            if dict_payload is not None:
                if dict_payload['request'] == 'logout':
                    self.disconnect()
                else:
                    payload = json.dumps(dict_payload)
                    self.send_payload(payload)
            else:
                print("Error, type 'help' to receive list of commands")

        
    def disconnect(self):
        payload  = json.dumps({'request':'logout'})
        self.send_payload(payload)
        sys.exit()

    def receive_message(self, message):
        print(self.parser.parse(message))


    def send_payload(self, data):
        self.connection.sendall(bytes(data, 'UTF-8'))
        
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
