from event_sourcing.projections.student_projector import project_students


def list_students():
    return project_students()

