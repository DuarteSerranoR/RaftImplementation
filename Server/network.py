from Server.server import Server


class Network:
    def Run(self, replicas, host, port):
        print("Hosting replica on: " + host + ":" + str(port))

        # server faz bind e listen
        self.server = Server(replicas)
        self.server.BindSocket(host, port)
        self.server.Listen()

    def CloseConnections(self):
        self.server.CloseSocket()
