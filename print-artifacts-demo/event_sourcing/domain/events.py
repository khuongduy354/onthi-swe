def student_added(student_id, name):
    return {"type": "StudentAdded", "data": {"id": student_id, "name": name}}


def score_recorded(student_id, subject, score):
    return {"type": "ScoreRecorded", "data": {"id": student_id, "subject": subject, "score": score}}

