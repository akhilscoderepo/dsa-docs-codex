import json


def build_trace(first, second):
    i = 0
    j = 0
    output = []
    steps = []
    while i < len(first) and j < len(second):
        left = max(first[i][0], second[j][0])
        right = min(first[i][1], second[j][1])
        if left <= right:
            output.append([left, right])
            note = f"The current pair overlaps at [{left},{right}], so emit it."
        else:
            note = f"The current pair has an empty overlap because {left} is greater than {right}."

        end_a = first[i][1]
        end_b = second[j][1]
        if end_a < end_b:
            note += f" A ends first at {end_a}; advance A because it cannot reach a later B interval."
            next_i, next_j = i + 1, j
        elif end_b < end_a:
            note += f" B ends first at {end_b}; advance B because it cannot reach a later A interval."
            next_i, next_j = i, j + 1
        else:
            note += f" Both end at {end_a}; advance both expired intervals."
            next_i, next_j = i + 1, j + 1

        steps.append(
            {
                "at": {"left": i, "right": j},
                "vars": {
                    "A": f"[{first[i][0]},{first[i][1]}]",
                    "B": f"[{second[j][0]},{second[j][1]}]",
                    "candidate": f"[{left},{right}]",
                    "emitted": len(output),
                },
                "note": note,
            }
        )
        i, j = next_i, next_j

    return {
        "cells": [f"A[{k}]=[{a},{b}]" for k, (a, b) in enumerate(first)]
        + [f"B[{k}]=[{a},{b}]" for k, (a, b) in enumerate(second)],
        "pointers": ["left", "right"],
        "steps": steps,
    }


if __name__ == "__main__":
    print(json.dumps(build_trace([[1, 4], [7, 10], [13, 17]], [[2, 5], [6, 8], [10, 14]]), separators=(",", ":")))
