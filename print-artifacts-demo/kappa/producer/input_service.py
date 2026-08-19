import uuid

from kappa.storage.event_log import append
from kappa.stream.processor import process_stream


def submit(category, amount):
    append({"eventId": str(uuid.uuid4())[:8], "category": category, "amount": amount, "time": "now"})
    return process_stream()

