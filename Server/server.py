import pickle
import random
import time
from typing import List

from Models.replica import Replica
from socket import *
import threading
from threading import Thread

global results
mutex = threading.Lock()


class Server:
    socketserver: socket
    replicas: List[Replica]
    signal: bool
    id: int
    state: str
    currentTerm: int  # TODO
    lastLogIndex: int  # TODO
    timer: int

    def __init__(self, replicas, selfId):
        self.id = selfId
        self.signal = False
        self.replicas = replicas
        self.state = "Follower"
        self.currentTerm = 0
        self.lastLogIndex = 0
        self.timer = random.randrange(10, 15, 1)
        time.sleep(15)  # TODO - awaits 15 seconds to start other replicas before election
        print("Starting server...")
        self.socketServer = socket(AF_INET, SOCK_STREAM)

    # Serverside - All replicas do
    def BindSocket(self, host, port):
        print("Binding replica's socket to " + host + ":" + str(port))
        self.socketServer.bind((host, port))

    def RequestVote(self):  # TODO - change implementation as follows in the RAFT paper
        print("Requesting new Leader Election")
        self.state = "Candidate"
        connect = False
        for replica in self.replicas:
            if not replica.Alive():
                connect = True
                break
        if connect:
            self.ConnectReplicas()
        Results = self.MajorityInvoke("RequestVote", "")
        leaderId = self.id
        bestCurrentTerm = self.currentTerm
        bestLogIndex = self.lastLogIndex
        for result in Results:
            (replicaId, label, data) = pickle.loads(result)
            (term, lastLogIndex) = pickle.loads(data)
            if lastLogIndex > bestLogIndex and bestCurrentTerm == term:  # TODO - revise
                leaderId = replicaId
        if leaderId == self.id:
            self.state = "Leader"

    def AppendEntries(self):  # TODO
        term = self.currentTerm

    def StartElection(self):  # TODO - delete and find different solution
        print("Starting new Leader Election")
        self.state = "Candidate"

    def Listen(self):
        print("Server listening...")
        self.socketServer.listen(len(self.replicas) + 1)
        leader = False
        while True:
            '''
            if self.state == "Leader" and not leader:
                self.ConnectReplicas()
                leader = True

            if self.state != "Leader" and leader:
                self.DisconnectReplicas()
                leader = False
            '''

            (clientsocket, address) = self.socketServer.accept()
            message = clientsocket.recv(65536)
            (SenderID, RequestLabel, RequestData) = pickle.loads(message)

            if RequestLabel == "RequestVote":
                self.StartElection()
            else:
                # if leader:
                if self.id == 0: # TODO
                    Result = self.MajorityInvoke(RequestLabel, RequestData)

                Result = self.processRequest(SenderID, RequestLabel, RequestData)

                response = pickle.dumps(Result)
                clientsocket.sendall(response)

                if self.signal:
                    break

    def processRequest(self, SenderID, RequestLabel, RequestData):
        ReplicaID = self.id
        Result = invoke(ReplicaID, RequestLabel, RequestData)
        (RequestLabel, EventHandler) = Result
        registerHandler(EventHandler, RequestLabel)
        return Result

    # Clientside - only the leader will connect to all replicas and invoke messages
    def ConnectReplicas(self):
        for i in range(len(self.replicas)):
            t = threading.Thread(target=self.replicas[i].Connect, args=())
            t.start()

    def DisconnectReplicas(self):
        for i in range(len(self.replicas)):
            t = threading.Thread(target=self.replicas[i].Dispose(), args=())
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
            if len(results) >= k:
                break

        return results

    def InvokeReplica(self, replicaId, requestLabel, requestData):
        global results
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


def WriteString(inputString):
    global string
    string = inputString


def ReadString():
    global string
    if string:
        return string
    else:
        return ""
