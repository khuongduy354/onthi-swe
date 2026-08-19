from event_sourcing.domain.events import score_recorded, student_added

EVENTS = [
    {"version": 1, **student_added("SV001", "Nguyễn An")},
    {"version": 2, **score_recorded("SV001", "Architecture", 8.5)},
]


def append(event):
    stored = {"version": len(EVENTS) + 1, **event}
    EVENTS.append(stored)
    return stored


def read_all():
    return list(EVENTS)

