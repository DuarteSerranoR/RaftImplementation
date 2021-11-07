from array import array
from Models.replica import Replica
from socket import *
import threading
from threading import Thread

global results
mutex = threading.Lock()


class Server:
    socketserver: socket
    replicas: array[Replica]
    signal: bool

    def __init__(self, replicas):
        self.signal = False
        self.replicas = replicas
        print("Starting server...")
        self.socketServer = socket(AF_INET, SOCK_STREAM)

    # Serverside - All replicas do
    def BindSocket(self, host, port):
        print("Binding replica's socket to " + host + ":" + str(port))
        self.socketServer.bind((host, port))

    def Listen(self):
        self.ConnectReplicas()
        print("Server listening...")
        while True:
            self.socketServer.listen(len(self.replicas))
            # TODO - will need to manage logs there (replicas), so it would be good to keep everything separate.
            #  Check the exercise's recommended methods.
            (clientsocket, address) = self.socketServer.accept()
            message = clientsocket.recv(1024).decode("utf-8")
            requestLabel = message
            requestData = message
            if requestLabel != 'Message received':
                result = self.ProcessRequest(clientsocket, address, requestLabel, requestData)
            # elif clientsocket.recv(1024):

            # else:
                # TODO - For logs - could send an 'ok' back. And if the other message didn't get the ok,
                #  it would keep sending (while not ok - with socket to listening
                #  [threading problems - use server socket and global vars])

            if self.signal:
                break

    def ProcessRequest(self, clientsocket, address, requestLabel, requestData):
        print("Received message from replica " + str(address))
        print("Request: " + requestLabel)
        try:
            clientsocket.sendall('Message received')
        except Exception as ex:
            print("Couldn't send back message. Error: %s" % ex)

        # If leader -> invoke/send to all the task before executing
        result = self.MajorityInvoke(requestLabel, requestData)

        # Then always execute task, even if not leader
        #...

        #TODO - check if is successful, if not - send as bytes-like object
        # and if not check if it is alive (connection)

        # TODO - registerHandler and EventHandler
        #  registerHandler(RequestLabel, EventHandler)

        return result

    # Clientside - only the leader will connect to all replicas and invoke messages
    def ConnectReplicas(self):
        for i in range(len(self.replicas)):
            t = threading.Thread(target=self.replicas[i].Connect, args=())
            t.start()

    def MajorityInvoke(self, requestLabel, requestData):  # TODO ------> What is requestLabel? <------
        global results
        results = [None] * len(self.replicas)  # Already excluding itself in the creation of the replicas
        t = []
        for i in range(len(self.replicas)):
            t.append(Thread(target=self.Invoke, args=(i, requestLabel, requestData)))
            t[i].start()

        # k = n/2 - 1
        # We should add 1 to the number of results (because we excluded itself already) and wait to get
        # this n/2 - 1 of results from the total n replicas

        # join will always wait for all, need another method - maybe use append on the array and wait
        # with a while cycle for there to be k number of array indexes.
        for i in range(len(t)):  # TODO - change methodology
            t[i].join()

        return results

    def Invoke(self, replicaId, requestLabel, requestData):
        result = self.replicas[replicaId].Invoke(requestLabel, requestData)
        mutex.acquire()
        results.insert(replicaId, result)
        mutex.release()
        return result

    # Disconnect and Dispose methods to get rid of all open sockets
    def Disconnect(self):  # TODO - not implemented
        self.signal = True

    def Dispose(self):
        # TODO - needs testing and checking if connections are open or if leader
        for replica in self.replicas:
            replica.Dispose()
        self.socketServer.close()
