import sys

from Models.replica import Replica
from Server.network import Network

# Parse replicas file
replicasFile = open("replicas", "r").read().splitlines()

# Store replicas variables
# And print existing replicas
replicas = []
host = "localhost"
port = 0
replicaId = -1
print("Current replicas:")
replicaProcessed = False
for i in range(len(replicasFile)):
    if i == int(sys.argv[1]):
        host = replicasFile[i].split(":")[0]
        port = int(replicasFile[i].split(":")[1])
        replicaId = i
        replicaProcessed = True
        continue
    else:
        if replicaProcessed:
            replicas.append(Replica(i, replicasFile[i]))
            replicas[i - 1].print()
        else:
            replicas.append(Replica(i, replicasFile[i]))
            replicas[i].print()

#for i in range(len(replicasFile)):
#    replicas.append(Replica(i, replicasFile[i]))
#    replicas[i].print()

# Network
# https://docs.python.org/3.8/howto/sockets.html
network = Network()
try:
    network.StartServer(replicas, host, port, replicaId)
except Exception as ex:
    print("Error: %s" % ex)
finally:
    try:
        network.Dispose()
    except Exception as ex:
        print("Couldn't init network")
        print("Error: %s" % ex)
