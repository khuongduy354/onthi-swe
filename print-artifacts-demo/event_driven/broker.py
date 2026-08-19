EVENT_LOG = []
PROCESSED = []


def publish(event):
    EVENT_LOG.append(event)
    consume(event)
    return event


def consume(event):
    if event["eventId"] not in {item["eventId"] for item in PROCESSED}:
        PROCESSED.append({**event, "consumer": "notification-service", "status": "processed"})

