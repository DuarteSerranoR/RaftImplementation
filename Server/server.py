import pickle
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
            (clientsocket, address) = self.socketServer.accept()
            message = clientsocket.recv(1024)
            (SenderID, RequestLabel, RequestData) = pickle.loads(message)
            # TODO - use ReplicaId to identify where the
            #  request came from (to know who the leader
            #  is)

            # TODO - change the tuple on the sending of the message too
            Result = self.MajorityInvoke(RequestLabel, RequestData)
            Result = self.processRequest(SenderID, RequestLabel, RequestData)

            if self.signal:
                break

    def processRequest(self, SenderID, RequestLabel, RequestData):
        ReplicaID = SenderID  # TODO - revise - use this.id when to replica id (also need to alter main)
        Result = invoke(ReplicaID, RequestLabel, RequestData)
        (RequestLabel, EventHandler) = Result
        registerHandler(EventHandler, RequestLabel)
        return Result

    # Clientside - only the leader will connect to all replicas and invoke messages
    def ConnectReplicas(self):
        for i in range(len(self.replicas)):
            t = threading.Thread(target=self.replicas[i].Connect, args=())
            t.start()

    def MajorityInvoke(self, requestLabel, requestData):
        global results
        results = []  # [None] * len(self.replicas)  # Already excluding itself in the creation of the replicas
        t = []
        for i in range(len(self.replicas)):
            t.append(Thread(target=self.InvokeReplica, args=(i, requestLabel, requestData)))
            t[i].start()

        # k = n/2 - 1
        n = len(self.replicas) + 1  # the +1 is the current replica
        k = n / 2 - 1

        while True:
            if len(results) == k:
                break

        return results

    def InvokeReplica(self, replicaId, requestLabel, requestData):
        result = self.replicas[replicaId].Invoke(self.id, requestLabel, requestData)
        mutex.acquire()
        results.append(result)
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


def invoke(ReplicaID, RequestLabel, RequestData):
    if RequestLabel == "WriteString":
        WriteString(RequestData)
        (RequestLabel, EventHandler) = (RequestLabel, "Operation executed with Success")
    elif RequestLabel == "ReadString":
        _ = ReadString()
        (RequestLabel, EventHandler) = (RequestLabel, _)
    else:
        (RequestLabel, EventHandler) = (RequestLabel, "Operation executed with Success")
    return RequestLabel, EventHandler


def registerHandler(RequestLabel, EventHandler):
    # TODO - log
    return


global string


def WriteString(string):
    string = string


def ReadString():
    return string
