import json


def prefix_trace(values):
    total = 0
    steps = []
    for i, value in enumerate(values):
        before = total
        total += value
        steps.append({"at": {"i": i}, "vars": {"before": before, "after": total},
                      "note": f"Extend boundary {i} with {value}."})
    return {"cells": values, "pointers": ["i"], "steps": steps}


if __name__ == "__main__":
    print(json.dumps(prefix_trace([3, -1, 4, 2]), separators=(",", ":")))
