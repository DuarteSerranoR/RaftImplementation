from socket import *
import time


class Server:
    def __init__(self, id):
        print("Starting new server " + str(id) + " ...")
        self.id = id
        self.networkSocket = socket(AF_INET, SOCK_STREAM)
        # self.networkSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)

    def BindSocket(self, host, port):
        print("Binding socket " + str(id) + " to " + host + ":" + str(port))
        self.networkSocket.bind((host, int(port)))

    def Run(self):
        print("Starting server...")
        while True:
            time.sleep(1)
