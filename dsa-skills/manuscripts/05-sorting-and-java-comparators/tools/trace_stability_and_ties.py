import json


def build_trace():
    return {
        "cells": ["Z-900:s1@0", "B-200:s2@1", "A-100:s1@2"],
        "pointers": ["earlier", "later"],
        "steps": [
            {"at": {"earlier": 0, "later": 2}, "vars": {"severity": "1 vs 1"}, "note": "The primary keys tie, so the severity comparator returns zero."},
            {"at": {"earlier": 0, "later": 2}, "vars": {"stable": "index 0 before 2"}, "note": "Stable sorting preserves Z-900 before A-100."},
            {"at": {"earlier": 2, "later": 1}, "vars": {"severity": "1 vs 2"}, "note": "A-100 moves ahead of the severity 2 alert."},
            {"at": {"earlier": 0, "later": 1}, "vars": {"order": "Z-900, A-100, B-200"}, "note": "The output groups severity while retaining encounter order inside the tied group."},
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build_trace(), separators=(",", ":")))
