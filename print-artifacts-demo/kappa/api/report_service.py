from kappa.storage.serving_db import read_report
from kappa.stream.processor import process_stream


def get_report():
    if not read_report():
        process_stream()
    return read_report()

