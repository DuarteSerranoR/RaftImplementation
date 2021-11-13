import pickle
from socket import *


class Client:
    def __init__(self, host, port):
        self.alive = False
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            print("Creating client for replica " + host + ":" + str(port))
            self.socket.connect((host, port))
            self.alive = True
        except:
            print("Couldn't connect to replica " + host + ":" + str(port))

    def SendMessage(self, SenderId, requestLabel, requestData):
        # TODO - fix me
        message = pickle.dumps((SenderId, requestLabel, requestData))
        print("Sending message...")
        self.socket.sendall(message)
        response = self.socket.recv(1024).decode("utf-8")
        print("Got replica's response " + response)
        return response

    def Dispose(self):
        self.socket.close()
        self.alive = False
