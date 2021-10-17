from Models.replica import Replica
from Server.network import Network

# Parse replicas file
replicasFile = open("replicas", "r").read().splitlines()

# Store replicas variables
# And print existing replicas
replicas = []
print("Current replicas:")
for i in range(len(replicasFile)):
    replicas.append(Replica(i, replicasFile[i]))
    replicas[i].print()


# TODO - Question about how the machine gets it's own port and trasnfers it to the file

# Network
# https://docs.python.org/3.8/howto/sockets.html
network = Network(replicas)
