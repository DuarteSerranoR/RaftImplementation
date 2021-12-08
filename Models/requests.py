def registerHandler(RequestLabel, RequestData):
    # TODO - log
    if RequestLabel == "WriteString":
        WriteString(RequestData)
        (RequestLabel, EventHandler) = (RequestLabel, "Operation executed with Success")
    elif RequestLabel == "ReadString":
        _ = ReadString()
        (RequestLabel, EventHandler) = (RequestLabel, _)
    else:
        (RequestLabel, EventHandler) = (RequestLabel, "Operation executed with Success")
    return RequestLabel, EventHandler  # TODO - 1 handler for each request label or 1 for all (different file) -> this will


global string


def WriteString(inputString):
    global string
    string = inputString


def ReadString():
    global string
    if string:
        return string
    else:
        return ""
