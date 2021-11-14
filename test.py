import pickle
import time
from socket import *

host = 'localhost'
port = 3009
sckt = socket(AF_INET, SOCK_STREAM)

SenderId = -1
requestLabel = 'WriteString'
requestData = "No more 'Hello World's"

message = pickle.dumps((SenderId, requestLabel, requestData))
print("Sending 1st message...")
sckt.connect((host, port))
time.sleep(1)
sckt.sendall(message)
response = pickle.loads(sckt.recv(65536))
sckt.detach()
sckt.close()

time.sleep(1)
print("Result: " + str(response))

SenderId = -1
requestLabel = 'ReadString'
requestData = ''

message = pickle.dumps((SenderId, requestLabel, requestData))
sckt = socket(AF_INET, SOCK_STREAM)
sckt.connect((host, port))
print("Sending 2nd message...")
time.sleep(1)
sckt.sendall(message)
response = pickle.loads(sckt.recv(65536))

print("Result: " + str(response))

sckt.close()
