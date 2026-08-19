from event_driven.infrastructure.in_memory_broker import subscribe

PROCESSED = []


def handle(event):
    if event["eventId"] not in {item["eventId"] for item in PROCESSED}:
        PROCESSED.append({**event, "consumer": "notification-service", "status": "processed"})


subscribe(handle)

