# -*- coding: utf-8 -*-
import socketserver
import json
import time
import re


"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
names = []
history = []
help_text = " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n" \
            "|USE THE FOLLOWING COMMANDS TO OPERATE THE CHAT SERVICE:|\n" \
            "|-------------------------------------------------------|\n" \
            "| login <username>  - log in with the given username    |\n" \
            "| logout            - log out                           |\n" \
            "| msg <message>     - send message                      |\n" \
            "| names             - list users in chat                |\n" \
            "| help              - view help text                    |\n" \
            " ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   "

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Every time a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """


    def handle(self):

        self.possible_requests = {
            'login': self.login,
            'logout': self.logout,
            'msg': self.message,
            'help': self.help,
            'history': self.history,
            'names': self.names
        }

        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.user_name = None

        names.append(self)

        # Loop that listens for messages from the client
        while True:
            rcvd_req = json.loads(self.connection.recv(4096).decode('UTF-8'))
            if rcvd_req['request'] in self.possible_requests:
                if self.user_name is None and rcvd_req['request'] not in['help','login']:
                    self.error("Not logged in.")
                elif rcvd_req == 'logout':
                    self.logout(rcvd_req)
                    break
                else:
                    self.possible_requests[rcvd_req['request']](rcvd_req)

    def login(self,request):
        if re.match("^[A-Za-z0-9_-]+$", request['content']):
            print(request)
            self.user_name = request['content']
            self.history(None)
            message = {'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': self.user_name +' joined the chat' }
            payload = json.dumps(message)
            for user in names:
                if user.user_name is not None:
                    user.send_payload(payload)
            history.append(message)
        else:
            self.error('Username not allowed')

    def logout(self,request):
        names.remove(self)
        self.connection.close()
        if self.user_name is not None:
            message = {'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': self.user_name +' left the chat' }
            payload = json.dumps(message)
            for user in names:
                if user.user_name is not None:
                    user.send_payload(payload)
            history.append(message)


    def history(self,request):
        payload = {'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': history}
        self.send_payload(json.dumps(payload))

    def message(self,request):
        message = json.dumps({'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'message', 'content': request['content']})
        payload = json.dumps(message)
        for user in names:
            if user.user_name is not None:
                user.send_payload(payload)
        history.append(message)

    def names(self,request):
        user_names = ''
        for user in names:
            if user.user_name is not None:
                user_names += user.user_name + ', '
        payload = json.dumps({'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': user_names})

    def help(self,request):
        payload = json.dumps({'timestamp': int(time.time()), 'sender': '[Server]', 'response': 'info', 'content': help_text})
        self.send_payload(payload)

    def send_payload(self,payload):
        self.connection.send(bytes(payload,'UTF-8'))

    def error(self,message):
        payload = json.dumps({'timestamp': int(time.time()), 'sender': '[Error]', 'response': 'error', 'content': message})
        self.send_payload(payload)





class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print ('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
