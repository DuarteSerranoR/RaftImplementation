from typing import List

from Server.server import Server
from Models.replica import Replica


class Network:
    replicas: List[Replica]
    server: Server

    def StartServer(self, replicas, host, port, replicaId):
        print("Hosting replica on: " + host + ":" + str(port))

        # server faz bind e listen
        self.server = Server(replicas, replicaId)
        self.server.BindSocket(host, port)
        self.server.Listen()

    def Dispose(self):
        self.server.Dispose()
