import re


def tokens(text):
    return set(re.findall(r"[a-z]+", text.lower()))

