import time

class TimedEvent:
    def __init__(self, timer = None):
        self.timeStamp = time.time() # time that this object was created

        self.currentTime = time.time()
        self.triggerTime = self.currentTime + timer

        self.timeRemaining = self.triggerTime - self.currentTime

        # if the timer is None then it has not been set and is therfore not active
        self.isActive = False
        if timer:
            self.isActive = True

        self.isTriggered = False
    

    def setTimer(self, timer):
        self.isActive = True
        self.isTriggered = False
        self.currentTime = time.time()
        self.triggerTime = self.currentTime + timer


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