from Server.client import *
from socket import *
import threading


class Server:
    def __init__(self, replicas):
        self.replicas = replicas
        print("Starting server...")
        self.socketServer = socket(AF_INET, SOCK_STREAM)

    def BindSocket(self, host, port):
        print("Binding replica's socket to " + host + ":" + str(port))
        self.socketServer.bind((host, port))

    def Listen(self):
        print("Server listening...")

        while True:
            self.socketServer.listen(len(self.replicas))
            # TODO - Use the replicas to connect sockets.
            #  Also - will need to manage logs there, so it would be good to keep everything separate.
            #  Check the exercise's recommended methods.
            (clientsocket, address) = self.socketServer.accept()
            message = clientsocket.recv(1024).decode("utf-8")
            if message != 'Message received':
                t = threading.Thread(target=self.ProcessRequest, args=(clientsocket, address, message))
                t.start()
            # elif clientsocket.recv(1024):

            # else:
                # TODO - For logs - could send an 'ok' back. And if the other message didn't get the ok,
                #  it would keep sending (while not ok - with socket to listening
                #  [threading problems - use server socket and global vars])

    def ProcessRequest(self, clientsocket, address, message):
        print("Received message from replica " + str(address))
        print("Message: " + message)
        try:
            clientsocket.sendall('Message received')
        except Exception as ex:
            print("Couldn't send back message. Error: %s" % ex)
        #TODO - check if is successful, if not - send as bytes-like object
        # and if not check if it is alive (connection)

        for replica in self.replicas:
            t = threading.Thread(target=Client, args=(replica.host, replica.port, message))
            t.start()

    def CloseSocket(self):
        self.socketServer.close()
