import json


def make_trace(rows, cols, update):
    row1, col1, row2, col2, weight = update
    diff = [[0] * (cols + 1) for _ in range(rows + 1)]
    steps = []

    writes = (
        (row1, col1, weight, "Start the rectangle at its top-left corner."),
        (row1, col2 + 1, -weight, "Cancel the effect immediately to the right."),
        (row2 + 1, col1, -weight, "Cancel the effect immediately below."),
        (row2 + 1, col2 + 1, weight, "Restore the region canceled twice at the diagonal corner."),
    )
    for r, c, delta, note in writes:
        diff[r][c] += delta
        steps.append({
            "at": {"r": r, "c": c},
            "vars": {"delta": delta, "stored": diff[r][c]},
            "note": note,
        })

    for r in range(rows):
        for c in range(cols):
            above = diff[r - 1][c] if r else 0
            left = diff[r][c - 1] if c else 0
            overlap = diff[r - 1][c - 1] if r and c else 0
            diff[r][c] += above + left - overlap
            steps.append({
                "at": {"r": r, "c": c},
                "vars": {
                    "corner": diff[r][c] - above - left + overlap,
                    "above": above,
                    "left": left,
                    "overlap": overlap,
                    "value": diff[r][c],
                },
                "note": f"Reconstruct cell ({r},{c}) from the signed corner state.",
            })

    return {
        "cells": [0] * (rows * cols),
        "pointers": ["r", "c"],
        "steps": steps,
    }


if __name__ == "__main__":
    print(json.dumps(make_trace(3, 4, (0, 1, 1, 2, 5)), separators=(",", ":")))
