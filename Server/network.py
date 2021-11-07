from array import array
from Server.server import Server
from Models.replica import Replica


class Network:
    replicas: array[Replica]
    server: Server

    def StartServer(self, replicas, host, port):
        print("Hosting replica on: " + host + ":" + str(port))

        # server faz bind e listen
        self.server = Server(replicas)
        self.server.BindSocket(host, port)
        self.server.Listen()

    def Dispose(self):
        self.server.Dispose()
        for i in range(len(self.replicas)):
            self.replicas[i].Dispose()
