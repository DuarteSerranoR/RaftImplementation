from Server.server import Server
from multiprocessing.pool import ThreadPool as Pool


class Network:
    def __init__(self, replicas):
        pool = Pool()
        for i in range(len(replicas)):
            pool.apply_async(self.ConnectSocket, (i, replicas[i]))

        pool.close()
        pool.join()

    def ConnectSocket(self, i, replica):
            server = Server(i)
            server.BindSocket(replica.host, replica.port)
            server.Run()

