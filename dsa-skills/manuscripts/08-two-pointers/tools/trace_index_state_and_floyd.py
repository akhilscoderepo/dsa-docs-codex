import json


def floyd_trace(nums):
    slow = fast = nums[0]
    steps = [{
        "at": {"slow": slow, "fast": fast},
        "vars": {"phase": "meeting", "moves": 0},
        "note": "Both positions start at the index named by nums[0].",
    }]

    moves = 0
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        moves += 1
        steps.append({
            "at": {"slow": slow, "fast": fast},
            "vars": {"phase": "meeting", "moves": moves},
            "note": "Slow follows one link; fast follows two links.",
        })
        if slow == fast:
            break

    slow = nums[0]
    entry_moves = 0
    steps.append({
        "at": {"slow": slow, "fast": fast},
        "vars": {"phase": "entry", "moves": entry_moves},
        "note": "Reset one position to nums[0] and keep the other at the meeting point.",
    })
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
        entry_moves += 1
        steps.append({
            "at": {"slow": slow, "fast": fast},
            "vars": {"phase": "entry", "moves": entry_moves},
            "note": "Equal-speed movement brings both positions to the cycle entry.",
        })

    return {
        "cells": nums,
        "pointers": ["slow", "fast"],
        "steps": steps,
    }


if __name__ == "__main__":
    print(json.dumps(floyd_trace([1, 4, 3, 2, 2]), separators=(",", ":")))
