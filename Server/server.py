import pickle
from time import sleep
from typing import List

from Models.state import State
from Models.replica import Replica
from Models.requests import registerHandler
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
    state: State

    def __init__(self, replicas, selfId):
        self.id = selfId
        self.signal = False
        self.replicas = replicas
        self.state = State(selfId)
        self.state.ChangeState("Candidate")
        #time.sleep(15)  # TODO - awaits 15 seconds to start other replicas before election
        print("Starting server...")
        self.socketServer = socket(AF_INET, SOCK_STREAM)

    # Serverside - All replicas do
    def BindSocket(self, host, port):
        print("Binding replica's socket to " + host + ":" + str(port))
        self.socketServer.bind((host, port))

    # def StartElection(self):  # TODO - change implementation as follows in the RAFT paper
    #     print("Requesting new Leader Election")
    #     self.state.state = "Candidate"
    #     connect = False
    #     for replica in self.replicas:
    #         if not replica.Alive():
    #             connect = True
    #             break
    #     if connect:
    #         self.ConnectReplicas()
    #     Results = self.MajorityInvoke("RequestVote", "") #use this request to change the replicas states
    #     leaderId = self.id                               #use another request to test replicas and get final result
    #     bestCurrentTerm = self.state.currentTerm
    #     bestLogIndex = self.state.lastLogIndex
    #     for result in Results:
    #         (replicaId, label, data) = pickle.loads(result)
    #         (term, lastLogIndex) = pickle.loads(data)
    #         if lastLogIndex > bestLogIndex and bestCurrentTerm == term:  # TODO - revise
    #             leaderId = replicaId
    #     if leaderId == self.id:
    #         self.state.state = "Leader"

    def AppendEntries(self):  # TODO
        #mutex acquire
        term = self.state.currentTerm
        #log
        self.state.lastLogIndex += 1
        #mutex release

    def RequestVote(self):  # TODO
        print("Starting new Leader Election")
        self.state.state = "Candidate"

    def Listen(self):
        print("Server listening...")
        self.socketServer.listen(len(self.replicas) + 1)
        Thread(target=self.LeaderElection, args=(True,)).start()
        while self.signal:
            (clientsocket, address) = self.socketServer.accept()
            message = clientsocket.recv(65536)
            (SenderID, RequestLabel, RequestData) = pickle.loads(message)

            while self.state.state == "Candidate":
                sleep(1)

            #TODO use sender id to check if it is a replica, if client and not leader return not leader
            if RequestLabel == "RequestVote":
                print("election")
            elif RequestLabel == "Heartbeat":
                if self.state.state == "Follower":
                    self.state.Beat()
            else:
                Result = self.processRequest(SenderID, RequestLabel, RequestData)
                response = pickle.dumps(Result)
                clientsocket.sendall(response)

    def LeaderElection(self, firstConnect):
        self.state.ChangeState("Candidate")
        if firstConnect:
            self.ConnectReplicas()
            self.MajorityInvoke(self.id, "Connected Replica", "")
            self.state.ChangeState(self.processRequest(self.id, "Connected Replica", ""))
            Thread(target=self.Heartbeat, args=()).start()

        #TODO - determine state

        if self.state.state == "Leader":
            self.ConnectReplicas()
        if self.state.state != "Leader":
            self.DisconnectReplicas()

    def Heartbeat(self):
        while True:
            while self.state.state == "Leader":
                self.MajorityInvoke(self.id, "Heartbeat", "")
                sleep(2.5)
            while self.state.state == "Candidate":
                if self.state.CheckBeatTimer():
                    self.state.LostHeartbeat = True
                else:
                    sleep(1)

    def processRequest(self, SenderID, RequestLabel, RequestData):
        ReplicaID = self.id
        if SenderID == -1 and self.state.state != "Leader":
            return "Leader -> " + str(self.state.leader)
        elif self.state.state == "Leader":
            self.MajorityInvoke(ReplicaID, RequestLabel, RequestData)
        selfResult = registerHandler(RequestLabel, RequestData)
        return selfResult

    # Clientside - only the leader will connect to all replicas and invoke messages
    def ConnectReplicas(self):
        for i in range(len(self.replicas)):
            self.replicas[i].Connect()
        numConnected = 0
        for replica in self.replicas:
            if replica.Alive():
                numConnected += 1
        sleep(10)
        # k = n/2 - 1
        n = len(self.replicas) + 1  # the +1 is the current replica
        k = n / 2 - 1
        if numConnected <= k:
            numConnected = 0
            for replica in self.replicas:
                if replica.Alive():
                    numConnected += 1
            # k = n/2 - 1
            n = len(self.replicas) + 1  # the +1 is the current replica
            k = n / 2 - 1
            if numConnected <= k:
                for i in range(len(self.replicas)):
                    self.replicas[i].Dispose()
                    self.ConnectReplicas()

    def DisconnectReplicas(self):
        for i in range(len(self.replicas)):
            t = threading.Thread(target=self.replicas[i].Dispose(), args=())
            t.start()

    def invoke(self, replicaNum, replicaId, requestLabel, requestData):
        global results
        result = self.replicas[replicaNum].Invoke(replicaId, requestLabel, requestData)
        mutex.acquire()
        results.append(result)
        mutex.release()
        return result

    def MajorityInvoke(self, replicaId, requestLabel, requestData):
        global results
        results = []  # [None] * len(self.replicas)  # Already excluding itself in the creation of the replicas
        t = []
        for i in range(len(self.replicas)):
            t.append(Thread(target=self.invoke, args=(i, replicaId, requestLabel, requestData)))
            t[i].start()

        # k = n/2 - 1
        n = len(self.replicas) + 1  # the +1 is the current replica
        k = n / 2 - 1

        while True:
            if len(results) >= k:
                break

        return results

    # Disconnect and Dispose methods to get rid of all open sockets
    def Disconnect(self):  # TODO - not implemented
        self.signal = True

    def Dispose(self):
        # TODO - needs testing and checking if connections are open or if leader
        for replica in self.replicas:
            replica.Dispose()
        self.socketServer.close()
