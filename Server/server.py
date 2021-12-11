import pickle
from time import sleep, time
from typing import List
from socket import *
import threading
from threading import Thread

from Models.state import State
from Models.replica import Replica
from Models.requests import registerHandler

global results
mutex = threading.Lock()


class Server:
    socketserver: socket
    replicas: List[Replica]
    signal: bool
    id: int
    state: State
    stopConnection: bool

    def __init__(self, replicas, selfId):
        self.id = selfId
        self.signal = True
        self.replicas = replicas
        self.state = State(selfId)
        self.state.ChangeState("Candidate")
        self.stopConnection = False
        print("Starting server...")
        self.socketServer = socket(AF_INET, SOCK_STREAM)

    # Serverside - All replicas do
    def BindSocket(self, host, port):
        print("Binding replica's socket to " + host + ":" + str(port))
        self.socketServer.bind((host, port))

    def AppendEntries(self):  # TODO
        # mutex acquire
        term = self.state.currentTerm
        # log
        self.state.lastLogIndex += 1
        # mutex release

    def Listen(self):
        print("Server listening...")
        self.socketServer.listen(len(self.replicas) + 1)
        Thread(target=self.LeaderElection, args=(True,)).start()
        while self.signal:
            try:
                (clientsocket, address) = self.socketServer.accept()
                message = clientsocket.recv(65536)
                if message == b'':
                    #print("Empty message received")
                    clientsocket.sendall(pickle.dumps("Empty message received"))
                    continue
                else:
                    (SenderID, RequestLabel, RequestData) = pickle.loads(message)

                # if self.state.state == "Candidate" and RequestLabel != "Start Election" and RequestLabel != "Set Leader":
                #     response = pickle.dumps("Leader election")
                #     clientsocket.sendall(response)
                if RequestLabel == "Start Election" and self.state.state == "Candidate":
                    self.stopConnection = True
                    response = pickle.dumps((self.id, self.state.currentTerm, self.state.lastLogIndex))
                    clientsocket.sendall(response)
                elif RequestLabel == "Start Election":
                    self.stopConnection = True
                    response = pickle.dumps((self.id, self.state.currentTerm, self.state.lastLogIndex))
                    clientsocket.sendall(response)
                    #self.LeaderElection(False,)
                elif RequestLabel == "Set Leader":
                    self.state.leader = RequestData
                    if self.id == RequestData:
                        self.state.ChangeState("Leader")
                    else:
                        self.state.ChangeState("Follower")
                    response = pickle.dumps("Leader Set")
                    clientsocket.sendall(response)
                elif RequestLabel == "Heartbeat":
                    if self.state.state == "Follower":
                        self.state.Beat()
                    response = pickle.dumps("Beat")
                    clientsocket.sendall(response)
                else:
                    Result = self.processRequest(SenderID, RequestLabel, RequestData)
                    print(str(SenderID) + "," + RequestLabel + "," + RequestData)
                    response = pickle.dumps(Result)
                    clientsocket.sendall(response)
            except Exception as ex:
                print("Fatal error -> %s" % ex)

    def LeaderElection(self, firstConnect):
        self.stopConnection = False
        if self.state.state == "Leader":
            self.DisconnectReplicas()
        self.state.ChangeState("Candidate")
        if not self.stopConnection:
            self.ConnectReplicas()
        if not self.stopConnection:
            notMajority = True
            while notMajority and not self.stopConnection and self.state.state == "Candidate":
                try:
                    replicas = self.MajorityInvoke(self.id, "Start Election", "")
                    leaderId = self.id
                    bestCurrentTerm = self.state.currentTerm
                    bestLogIndex = self.state.lastLogIndex
                    for result in replicas:
                        (replicaId, currentTerm, lastLogIndex) = pickle.loads(result)
                        if lastLogIndex > bestLogIndex and bestCurrentTerm == currentTerm:  # TODO - revise
                            leaderId = replicaId
                    self.MajorityInvoke(self.id, "Set Leader", leaderId)
                    self.state.leader = leaderId
                    if leaderId == self.id:
                        self.state.ChangeState("Leader")
                    else:
                        self.state.ChangeState("Follower")
                    notMajority = False
                except Exception as ex:
                    print("Could not send message -> %s" % ex)
                    sleep(30)
        self.DisconnectReplicas()
        if firstConnect:
            Thread(target=self.Heartbeat, args=()).start()

        while self.state.state == "Candidate":
            print("Determining State")

        self.stopConnection = False
        if self.state.state == "Leader":
            self.ConnectReplicas()

    def Heartbeat(self):
        while True:
            while self.state.state == "Leader":
                if self.state.ReElectionTimer():
                    self.LeaderElection(False)
                try:
                    self.MajorityInvoke(self.id, "Heartbeat", "")
                except Exception as ex:
                    print("Heartbeat error: %s" % ex)
                    try:
                        self.DisconnectReplicas()
                        self.ConnectReplicas()
                        self.MajorityInvoke(self.id, "Set Leader", self.id)
                        self.MajorityInvoke(self.id, "Heartbeat", "")
                    except:
                        print("Cannot reach replicas")
                sleep(2.5)
            while self.state.state == "Follower":
                if self.state.CheckBeatTimer():
                    self.LeaderElection(False)
                else:
                    sleep(1)

    def processRequest(self, SenderID, RequestLabel, RequestData):
        ReplicaID = self.id
        if SenderID == -1 and self.state.state != "Leader":
            return "Leader -> " + str(self.state.leader)
        elif self.state.state == "Leader":
            try:
                self.MajorityInvoke(ReplicaID, RequestLabel, RequestData)
                selfResult = registerHandler(RequestLabel, RequestData)
            except Exception as ex:
                selfResult = "Error: %s" % ex
        else:
            selfResult = registerHandler(RequestLabel, RequestData)

        return selfResult

    # Clientside - only the leader will connect to all replicas and invoke messages
    def ConnectReplicas(self):
        if self.stopConnection:
            return
        for i in range(len(self.replicas)):
            self.replicas[i].Connect()
        numConnected = 0
        for replica in self.replicas:
            if replica.Alive():
                numConnected += 1
        sleep(1)
        # k = n/2 - 1
        n = len(self.replicas)  # + 1  # the +1 is the current replica
        k = n / 2  # + 1
        if numConnected <= k:
            numConnected = 0
            for replica in self.replicas:
                if replica.Alive():
                    numConnected += 1

            # k = n/2 + 1
            n = len(self.replicas)  # + 1  # the +1 is the current replica
            k = (n / 2) + 1
            if numConnected <= k and not self.stopConnection:
                for i in range(len(self.replicas)):
                    self.replicas[i].Reconnect()
                    self.ConnectReplicas()
            elif self.stopConnection:
                self.DisconnectReplicas()

    def invoke(self, replicaNum, replicaId, requestLabel, requestData):
        global results
        try:
            result = self.replicas[replicaNum].Invoke(replicaId, requestLabel, requestData)
            mutex.acquire()
            results.append(result)
            mutex.release()
        except Exception as ex:
            print("Replica num " + str(replicaId + 1) + " didn't respond. Exception: %s", ex)

    def MajorityInvoke(self, replicaId, requestLabel, requestData):
        global results
        results = []  # [None] * len(self.replicas)  # Already excluding itself in the creation of the replicas
        t = []
        for i in range(len(self.replicas)):
            t.append(Thread(target=self.invoke, args=(i, replicaId, requestLabel, requestData)))
            t[i].start()

        # k = n/2 - 1
        n = len(self.replicas)  # + 1  # the +1 is the current replica
        k = (n / 2) + 1

        timeoutSecs = 40
        start = time()
        while True:
            if len(results) >= k:
                break
            elif timeoutSecs < time() - start:
                raise Exception("Majority not achieved")

        return results

    def DisconnectReplicas(self):
        for i in range(len(self.replicas)):
            t = threading.Thread(target=self.replicas[i].Dispose(), args=())
            t.start()

    # Disconnect and Dispose methods to get rid of all open sockets
    def Dispose(self):
        self.signal = True
        if self.state.state == "Leader":
            self.DisconnectReplicas()
        self.socketServer.close()
