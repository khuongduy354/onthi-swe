REPORT_ROWS = []


def replace(rows):
    REPORT_ROWS[:] = rows


def read_report():
    return list(REPORT_ROWS)

