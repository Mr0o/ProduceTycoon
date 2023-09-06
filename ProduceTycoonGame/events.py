from collections import defaultdict

# Default value of the dictionary will be list
subscribers = defaultdict(list)

# Every event that is posted will be appended to this list
eventList = []


def subscribe(eventType: str, fn):
    subscribers[eventType].append(fn)

# args
def postEvent(eventType: str, args):
    # append event to eventList
    eventList.append(eventType)

    # call subcribers function
    if not eventType in subscribers:
        return
    for fn in subscribers[eventType]:
        fn(args)

# no args
def postEvent(eventType: str):
    # append event to eventList
    eventList.append(eventType)

    # call subcribers function
    if not eventType in subscribers:
        return
    for fn in subscribers[eventType]:
        fn()

# clear the eventList
def clearEventList():
    eventList.clear()

# check if an event is in the eventList
def eventOccured(eventType: str) -> bool:
    return eventType in eventList
    