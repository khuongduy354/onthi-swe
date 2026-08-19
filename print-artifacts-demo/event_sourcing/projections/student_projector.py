from event_sourcing.domain.student import apply
from event_sourcing.infrastructure.event_store import read_all


def project_students():
    students = {}
    for event in read_all():
        student_id = event["data"]["id"]
        students[student_id] = apply(students.get(student_id, {}), event)
    return list(students.values())

