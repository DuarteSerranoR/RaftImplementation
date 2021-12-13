import pickle
from time import sleep
from socket import *
from threading import Thread


def request(message):
    host = "localhost"
    #ports = [2001, 1231, 3231, 2312, 1234]
    notSent = True
    response = ""
    #i = 0
    #while notSent:
    #port = ports[i]
    port = 1234
    sckt = socket(AF_INET, SOCK_STREAM)
    sckt.connect((host, port))
    sckt.sendall(message)
    response = pickle.loads(sckt.recv(65536))
    #if not response.startswith("Leader -> "):
    #    notSent = False
    sckt.close()
        #i += 1
    return response


def Incremental(stopping):
    i = 1
    while True:
        SenderId = -1
        requestLabel = 'Increment'
        requestData = ""

        message = pickle.dumps((SenderId, requestLabel, requestData))
        print("Sending message num {}...".format(str(i)))
        response = request(message)
        print("Result: " + str(response))
        i += 1
        sleep(4)
        if stopping and i == 10:
            break


SenderId = -1
requestLabel = 'WriteString'
requestData = "No more 'Hello World's"

message = pickle.dumps((SenderId, requestLabel, requestData))
print("Sending 1st message...")
response = request(message)
print("Result: " + str(response))
sleep(1)

SenderId = -1
requestLabel = 'ReadString'
requestData = ''

message = pickle.dumps((SenderId, requestLabel, requestData))
print("Sending 2nd message...")
response = request(message)

print("Result: " + str(response))

print("Starting sequential incremental function...")
Incremental(True)

print("Starting parallel incremental function...")
Thread(target=Incremental, args=(False,)).start()
Incremental(False)
