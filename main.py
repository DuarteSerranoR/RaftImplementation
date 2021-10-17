import os
from _socket import socket
from replica import Replica

# Parse replicas file
replicasFile = open("replicas", "r").read().splitlines()

# Store replicas variables
replicas = []
for replica in replicasFile:
    replicas.append(Replica(replica))

# Print existing replicas
print("Current replicas:")
for i in range(len(replicas)):
    replicas[i].print(i)

# Network
# https://docs.python.org/3.8/howto/sockets.html

# serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# replicas[]=