CHECKPOINTS = {}


def save(run_id, state):
    CHECKPOINTS[run_id] = dict(state)


def load(run_id):
    return CHECKPOINTS.get(run_id)

