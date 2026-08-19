from event_sourcing.domain.events import student_added
from event_sourcing.infrastructure.event_store import append


def add_student(student_id, name):
    return append(student_added(student_id, name))

