from kappa.storage.event_log import replay
from kappa.storage.checkpoint_store import save
from kappa.storage.serving_db import replace


def process_stream():
    result = {}
    for event in replay():
        row = result.setdefault(event["category"], {"category": event["category"], "count": 0, "sum": 0})
        row["count"] += 1
        row["sum"] += event["amount"]
    rows = list(result.values())
    replace(rows)
    save(len(replay()) - 1)
    return rows
