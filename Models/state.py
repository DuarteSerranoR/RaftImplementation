import random
import time


class State:
    id: int
    state: str
    time: int
    timer: float
    currentTerm: int  # TODO
    lastLogIndex: int  # TODO
    leader: int

    def __init__(self, id):
        self.id = id
        self.state = "Candidate"
        self.currentTerm = 0
        self.lastLogIndex = 0

    def ChangeState(self, state):
        if state == "Follower":
            print("Elected Follower")
            self.currentTerm = 0
            self.time = random.randrange(10, 15, 1)
            self.timer = time.time()
        elif state == "Leader":
            print("Elected Leader")
            self.currentTerm = 0

            # To reelect a leader
            self.time = random.randrange(320, 640)
            self.timer = time.time()
        else:
            print("Starting Election")
        self.state = state

    def CheckBeatTimer(self):
        now = time.time()
        secDif = now - self.timer
        if float(self.time) > secDif:
            return False
        else:
            return True

    def ReElectionTimer(self):
        now = time.time()
        secDif = now - self.timer
        if float(self.time) > secDif:
            return False
        else:
            return True

    def Beat(self):
        self.time = random.randrange(10, 15, 1)
        self.timer = time.time()

    #def ManageState(self):
    #    #while self.running:
    #    if self.state == "Candidate":
    #        self.election = True
    #    elif self.state == "Leader":
    #        AppendEntries()

