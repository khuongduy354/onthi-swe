RAW_EVENTS = [
    {"eventId": "e-001", "category": "Hotel", "amount": 120, "time": "09:00:02"},
    {"eventId": "e-002", "category": "Hotel", "amount": 80, "time": "09:00:04"},
    {"eventId": "e-003", "category": "Flight", "amount": 240, "time": "09:00:07"},
    {"eventId": "e-004", "category": "Hotel", "amount": 100, "time": "09:00:09"},
]


def append(event):
    if event["eventId"] not in {row["eventId"] for row in RAW_EVENTS}:
        RAW_EVENTS.append(event)


def replay():
    return list(RAW_EVENTS)

