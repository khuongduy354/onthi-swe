EVENT_LOG = []
SUBSCRIBERS = []


def subscribe(handler):
    SUBSCRIBERS.append(handler)


def publish(event):
    EVENT_LOG.append(event)
    for handler in SUBSCRIBERS:
        handler(event)
    return event

