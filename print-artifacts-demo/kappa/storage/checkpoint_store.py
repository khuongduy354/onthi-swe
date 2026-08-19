CHECKPOINT = {"offset": -1}


def save(offset):
    CHECKPOINT["offset"] = offset


def load():
    return CHECKPOINT["offset"]

