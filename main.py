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
print("Current replicas:")
for i in range(len(replicasFile)):
    if i == int(sys.argv[1]):
        host = replicasFile[i].split(":")[0]
        port = int(replicasFile[i].split(":")[1])
        replicasFile.pop(i)
        continue

for i in range(len(replicasFile)):
    replicas.append(Replica(i, replicasFile[i]))
    replicas[i].print()

# Network
# https://docs.python.org/3.8/howto/sockets.html
network = Network()
try:
    network.StartServer(replicas, host, port)
except Exception as ex:
    print("Error: %s" % ex)
finally:
    try:
        network.Dispose()
    except Exception as ex:
        print("Couldn't init network")
        print("Error: %s" % ex)
