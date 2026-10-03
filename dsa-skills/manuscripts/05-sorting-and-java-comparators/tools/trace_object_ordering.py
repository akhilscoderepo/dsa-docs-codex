import json


def build_trace():
    return {
        "cells": ["Mira:92", "Ben:85", "Ana:92"],
        "pointers": ["left", "right"],
        "steps": [
            {"at": {"left": 0, "right": 1}, "vars": {"score": "92 vs 85"}, "note": "The score comparison decides immediately: Mira belongs before Ben."},
            {"at": {"left": 2, "right": 0}, "vars": {"score": "92 vs 92"}, "note": "Equal scores transfer ownership to the name key."},
            {"at": {"left": 2, "right": 0}, "vars": {"name": "Ana vs Mira"}, "note": "Ana is lexicographically smaller, so Ana belongs before Mira."},
            {"at": {"left": 0, "right": 2}, "vars": {"order": "Ana, Mira, Ben"}, "note": "The completed order is score descending and name ascending within ties."},
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build_trace(), separators=(",", ":")))
