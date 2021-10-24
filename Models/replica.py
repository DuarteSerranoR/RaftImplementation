class Replica:
    def __init__(self, id, replica):
        self.id = int(id)
        split_string = replica.split(":")
        self.host = split_string[0]
        self.port = int(split_string[1])

    def print(self):
        print("Replica " + str(self.id + 1) + " -> " + self.host + ":" + str(self.port))
