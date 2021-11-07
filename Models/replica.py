from Server.client import Client


class Replica:
    id: int
    host: str
    port: int
    client: Client

    def __init__(self, id, replicaData):
        self.id = int(id)
        split_string = replicaData.split(":")
        self.host = split_string[0]
        self.port = int(split_string[1])

    def print(self):
        print("Replica " + str(self.id + 1) + " -> " + self.host + ":" + str(self.port))

    def Connect(self):
        self.client = Client(self.host, self.port)

    def Alive(self):
        return self.client.alive

    def Invoke(self, requestLabel, requestData):
        return self.client.SendMessage(requestLabel, requestData)

    def Dispose(self):
        self.client.Dispose()
