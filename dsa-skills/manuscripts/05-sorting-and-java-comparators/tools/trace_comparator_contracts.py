import json


def int32(value):
    value &= 0xFFFFFFFF
    return value if value < 0x80000000 else value - 0x100000000


def build_trace():
    low = -2_147_483_648
    high = 2_147_483_647
    bad = int32(low - high)
    safe = -1 if low < high else 1 if low > high else 0
    return {
        "cells": ["MIN", "0", "MAX"],
        "pointers": ["a", "b"],
        "steps": [
            {"at": {"a": 0, "b": 2}, "vars": {"a-b": bad}, "note": "Subtraction overflows to 1, falsely placing MIN after MAX."},
            {"at": {"a": 0, "b": 2}, "vars": {"compare": safe}, "note": "Integer.compare returns -1, so MIN correctly belongs first."},
            {"at": {"a": 1, "b": 1}, "vars": {"compare": 0}, "note": "Comparing a value with itself returns zero."},
            {"at": {"a": 2, "b": 0}, "vars": {"compare": 1}, "note": "Reversing the arguments reverses the sign."},
        ],
    }


if __name__ == "__main__":
    print(json.dumps(build_trace(), separators=(",", ":")))
