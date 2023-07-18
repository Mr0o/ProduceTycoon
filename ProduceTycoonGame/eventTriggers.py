import time

class TimedEvent:
    def __init__(self, seconds: int = 0):
        self.timeStamp = time.time() # time that this object was created

        self.currentTime = time.time()
        self.triggerTime = self.currentTime + seconds

        self.timeRemaining = self.triggerTime - self.currentTime

        # if the seconds is None then it has not been set and is therfore not active
        self.isActive = False
        if seconds:
            self.isActive = True

        self.isTriggered = False
    

    def setTimer(self, seconds: int):
        self.isActive = True
        self.isTriggered = False
        self.currentTime = time.time()
        self.triggerTime = self.currentTime + seconds


    def cancleTimer(self):
        self.isActive = False
        self.isTriggered = False


    def update(self):
        if self.isActive:
            self.currentTime = time.time()
            self.timeRemaining =  self.triggerTime - self.currentTime

            if self.currentTime > self.triggerTime:
                self.isTriggered = True
                self.isActive = False