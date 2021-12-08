import random
import time


class State:
    id: int
    state: str
    time: float
    timer: float
    LostHeartbeat: bool
    currentTerm: int  # TODO
    lastLogIndex: int  # TODO
    leader: int

    def __init__(self, id):
        self.id = id
        self.lastLogIndex = 0
        self.LostHeartbeat = False

    def ChangeState(self, state):
        self.state = state
        if state == "Follower":
            print("Elected Follower")
            self.currentTerm = 0
            self.time = random.randrange(10, 15, 1)
            self.timer = time.time()
        elif state == "Leader":
            print("Elected Leader")
            self.currentTerm = 0
            self.time = 0
        else:
            print("Starting Election")

    def CheckBeatTimer(self):
        if self.time > time.time() - self.timer:
            self.time = random.randrange(10, 15, 1)
            self.timer = time.time()
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

