DEAD_LETTERS = []


def send(event, reason):
    DEAD_LETTERS.append({"event": event, "reason": reason})

