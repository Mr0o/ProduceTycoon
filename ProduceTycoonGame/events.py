from collections import defaultdict

# Default value of the dictionary will be list
subscribers = defaultdict(list)

# Every event that is posted will be appended to this list
eventList: list['Event'] = []

debug = True

def subscribe(eventType: 'Event', fn):
    subscribers[eventType].append(fn)

# post using an Event object
def postEvent(event: 'Event'):
    # append event to eventList
    eventList.append(event)
    
    if debug:
        print(f"Event Posted\nEvent: {event.eventType} args: {event.args} data: {event.eventData}")

    # call subcribers function
    if not event in subscribers:
        return
    for fn in subscribers[event]:
        if debug:
            print(f"Function called on event: {event.eventType}")
            print(f"Function: {fn.__name__}")

        fn()

# post without passing an Event object
def postEvent(eventType: str, args=None, eventData=None):
    # create the Event object
    event = Event(eventType, args, eventData)

    # append event to eventList
    eventList.append(event)

    if debug:
        print(f"Event Posted\nEvent: {event.eventType} args: {event.args} data: {event.eventData}")

    # call subcribers function
    if not event in subscribers:
        return
    for fn in subscribers[event]:
        if debug:
            print(f"Function called on event: {event.eventType}")
            print(f"Function: {fn.__name__}")

        fn()


# clear the eventList (should be called at the beginning of every frame)
def clearEventList():
    eventList.clear()


# check if an event is in the eventList
def eventOccured(eventType: str) -> bool:
    # check if any of the event objects have the same eventType string
    for event in eventList:
        if event.getEventType() == eventType:
            return True
    
    return False


def getEvent(eventType: str) -> 'Event':
    # check if any of the event objects have the same eventType string
    for event in eventList:
        if event.getEventType() == eventType:
            return event
        
    return None

# event class
class Event:
    def __init__(self, eventType: str, args=None, eventData=None):
        self.eventType = eventType
        self.args = args

        # this can be used to store relevent event data such as x and y coords, etc.
        self.eventData = eventData

    def getEventType(self) -> str:
        return self.eventType

    def getArgs(self):
        return self.args
    
    def getData(self):
        return self.eventData

    def __str__(self):
        return self.eventType