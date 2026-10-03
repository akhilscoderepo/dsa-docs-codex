import json


def build_trace():
    return {
        "cells": [1, 1, 1, 2, 4, 4],
        "pointers": ["read", "write"],
        "steps": [
            {"at": {"read": 0, "write": 0}, "vars": {"emit": 1}, "note": "Index zero begins the first run, so write representative 1."},
            {"at": {"read": 1, "write": 1}, "vars": {"value": 1}, "note": "This 1 equals its predecessor and remains inside the current run."},
            {"at": {"read": 2, "write": 1}, "vars": {"value": 1}, "note": "A third 1 is skipped for the same reason."},
            {"at": {"read": 3, "write": 1}, "vars": {"emit": 2}, "note": "Two differs from one, marking a new run boundary."},
            {"at": {"read": 4, "write": 2}, "vars": {"emit": 4}, "note": "Four begins the final run and becomes its representative."},
            {"at": {"read": 5, "write": 3}, "vars": {"value": 4}, "note": "The final duplicate is skipped; the written prefix is [1,2,4]."},
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build_trace(), separators=(",", ":")))
