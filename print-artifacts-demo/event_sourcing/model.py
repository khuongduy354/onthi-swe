EVENTS = [
    {"version": 1, "type": "StudentAdded", "data": {"id": "SV001", "name": "Nguyễn An"}},
    {"version": 2, "type": "ScoreRecorded", "data": {"id": "SV001", "subject": "Architecture", "score": 8.5}},
]


def append(event_type, data):
    event = {"version": len(EVENTS) + 1, "type": event_type, "data": data}
    EVENTS.append(event)
    return event


def project():
    students = {}
    for event in EVENTS:
        data = event["data"]
        if event["type"] == "StudentAdded":
            students[data["id"]] = {"id": data["id"], "name": data["name"], "score": None}
        elif event["type"] == "ScoreRecorded":
            students[data["id"]]["score"] = data["score"]
    return list(students.values())

