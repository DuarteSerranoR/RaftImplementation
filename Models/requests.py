import threading
from time import sleep


def registerHandler(RequestLabel, RequestData):
    if RequestLabel == "WriteString":
        WriteString(RequestData)
        (RequestLabel, EventHandler) = (RequestLabel, "Operation executed with Success")
    elif RequestLabel == "ReadString":
        _ = ReadString()
        (RequestLabel, EventHandler) = (RequestLabel, _)
    elif RequestLabel == "Increment":
        _ = Increment()
        (RequestLabel, EventHandler) = (RequestLabel, _)
    else:
        (RequestLabel, EventHandler) = (RequestLabel, "Operation executed with Success")
    return RequestLabel, EventHandler


global string
global integer
mutexIncrement = threading.Lock()


def WriteString(inputString):
    global string
    string = inputString


def ReadString():
    global string
    if string:
        return string
    else:
        return ""


def Increment():
    global integer
    mutexIncrement.acquire()
    sleep(0.01)
    try:
        if integer is None:
            integer = 0
    except:
        integer = 0
    integer += 1
    mutexIncrement.release()
    return integer
