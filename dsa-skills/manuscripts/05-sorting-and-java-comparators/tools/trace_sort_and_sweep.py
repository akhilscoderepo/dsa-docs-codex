import json


def build_trace():
    return {
        "cells": [1, 1, 2, 2, 3, 7],
        "pointers": ["scan", "frontier"],
        "steps": [
            {"at": {"scan": 0, "frontier": 0}, "vars": {"requested": 1, "assigned": 1, "moves": 0}, "note": "Accept the first value and establish the frontier at 1."},
            {"at": {"scan": 1, "frontier": 1}, "vars": {"requested": 1, "assigned": 2, "moves": 1}, "note": "Raise the duplicate 1 to the smallest free value, 2."},
            {"at": {"scan": 2, "frontier": 2}, "vars": {"requested": 2, "assigned": 3, "moves": 2}, "note": "The requested 2 is occupied, so the frontier advances to 3."},
            {"at": {"scan": 3, "frontier": 3}, "vars": {"requested": 2, "assigned": 4, "moves": 4}, "note": "The next duplicate crosses the frontier and adds two moves."},
            {"at": {"scan": 4, "frontier": 4}, "vars": {"requested": 3, "assigned": 5, "moves": 6}, "note": "Assign 5; the finalized prefix remains minimally increasing."},
            {"at": {"scan": 5, "frontier": 5}, "vars": {"requested": 7, "assigned": 7, "moves": 6}, "note": "Seven already lies beyond the frontier, so no increment is needed."},
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build_trace(), separators=(",", ":")))
