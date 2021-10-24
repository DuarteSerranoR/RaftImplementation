from socket import *


def Client(host, port, message):
    s = socket(AF_INET, SOCK_STREAM)
    try:
        try:
            print("Creating client for replica " + host + ":" + str(port))
            s.connect((host, port))
            print("Sending message...")
            s.sendall(message)
            response = s.recv(1024).decode("utf-8")
            print("Got replica's response " + response)
        except:
            print("Couldn't connect to replica " + host + ":" + str(port))
        finally:
            s.close()
    except:
        print("No need to close connection")
