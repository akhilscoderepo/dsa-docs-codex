import json


def build_trace(matrix):
    rows, cols = len(matrix), len(matrix[0])
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    steps = []
    for r in range(rows):
        for c in range(cols):
            above = prefix[r][c + 1]
            left = prefix[r + 1][c]
            overlap = prefix[r][c]
            prefix[r + 1][c + 1] = matrix[r][c] + above + left - overlap
            steps.append({
                "at": {"r": r, "c": c},
                "vars": {
                    "cell": matrix[r][c],
                    "above": above,
                    "left": left,
                    "overlap": overlap,
                    "prefix": prefix[r + 1][c + 1],
                },
                "note": f"Build the origin rectangle ending at ({r},{c}); subtract the overlap once.",
            })

    r1, c1, r2, c2 = 1, 1, 2, 2
    total = prefix[r2 + 1][c2 + 1]
    top = prefix[r1][c2 + 1]
    left = prefix[r2 + 1][c1]
    overlap = prefix[r1][c1]
    steps.append({
        "at": {"r": r2, "c": c2},
        "vars": {"total": total, "top": top, "left": left, "overlap": overlap,
                 "answer": total - top - left + overlap},
        "note": "Query rows 1..2 and columns 1..2; restore the top-left overlap after removing two strips.",
    })
    return {
        "cells": [value for row in matrix for value in row],
        "pointers": ["r", "c"],
        "steps": steps,
    }


if __name__ == "__main__":
    print(json.dumps(build_trace([[2, -1, 4], [3, 5, 0], [-2, 6, 1]]), separators=(",", ":")))
