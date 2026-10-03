import json


def build_trace():
    return {"cells": [1, 2, 2, 3], "pointers": ["scan", "neighbor"], "steps": [
        {"at": {"scan": 3, "neighbor": 3}, "vars": {"value": 3, "rank": 1, "maximum": 3}, "note": "The greatest value establishes rank one and the fallback maximum."},
        {"at": {"scan": 2, "neighbor": 3}, "vars": {"value": 2, "rank": 2}, "note": "Two differs from three, so it begins the second distinct run."},
        {"at": {"scan": 1, "neighbor": 2}, "vars": {"value": 2, "rank": 2}, "note": "The duplicate two stays inside the current run and does not advance rank."},
        {"at": {"scan": 0, "neighbor": 1}, "vars": {"value": 1, "rank": 3}, "note": "One begins the third distinct run and is returned."},
    ]}


if __name__ == "__main__":
    print(json.dumps(build_trace(), separators=(",", ":")))
