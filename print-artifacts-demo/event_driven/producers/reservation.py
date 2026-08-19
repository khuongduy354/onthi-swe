import uuid

from event_driven.contracts.events import reservation_created
from event_driven.infrastructure.in_memory_broker import publish


def publish_reservation(hotel_id):
    event = reservation_created(str(uuid.uuid4())[:8], hotel_id)
    return publish(event)

