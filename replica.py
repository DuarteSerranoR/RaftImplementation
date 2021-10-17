class Replica:
    def __init__(self, replica):
        split_string = replica.split(":")
        self.ip = split_string[0]
        self.port = split_string[1]

    def print(self, i):
        print("Replica " + i.__str__() + " -> " + self.ip + ":" + self.port)
