import json


def difference_trace(length, updates):
    delta = [0] * (length + 1)
    steps = []

    for update_index, (left, right, value) in enumerate(updates):
        delta[left] += value
        delta[right + 1] -= value
        steps.append({
            "at": {"left": left, "right": right},
            "vars": {
                "update": update_index + 1,
                "value": value,
                "startDelta": delta[left],
                "stopDelta": delta[right + 1],
            },
            "note": (
                f"Record {value:+d} at boundary {left} and "
                f"{-value:+d} at boundary {right + 1}."
            ),
        })

    running = 0
    for index in range(length):
        running += delta[index]
        steps.append({
            "at": {"i": index},
            "vars": {"delta": delta[index], "running": running},
            "note": f"Reconstruct index {index}; its final value is {running}.",
        })

    return {
        "cells": [0] * length,
        "pointers": ["left", "right", "i"],
        "steps": steps,
    }


if __name__ == "__main__":
    print(json.dumps(
        difference_trace(6, [(1, 4, 3), (3, 5, -1), (0, 2, 2)]),
        separators=(",", ":"),
    ))
