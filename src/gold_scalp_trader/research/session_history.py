from collections import defaultdict
def group_by_session(rows):
    out=defaultdict(list)
    for row in rows:out[row["session"]].append(row)
    return dict(out)
