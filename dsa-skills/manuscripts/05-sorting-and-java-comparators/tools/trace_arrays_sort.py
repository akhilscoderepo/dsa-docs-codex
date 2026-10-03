import json


def insertion_trace(values):
    a = values[:]
    steps = [{"at": {"sorted": 0, "scan": 0}, "vars": {"key": a[0]}, "note": "A one-value prefix is already ordered."}]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        steps.append({"at": {"sorted": i - 1, "scan": i}, "vars": {"key": key}, "note": f"Take {key}; indices 0 through {i - 1} are the ordered prefix."})
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            steps.append({"at": {"sorted": i, "scan": j}, "vars": {"key": key}, "note": f"Shift {a[j]} right because it is greater than {key}."})
            j -= 1
        a[j + 1] = key
        steps.append({"at": {"sorted": i, "scan": j + 1}, "vars": {"key": key}, "note": f"Insert {key}; indices 0 through {i} are ordered."})
    return {"cells": values, "pointers": ["sorted", "scan"], "steps": steps}


if __name__ == "__main__":
    print(json.dumps(insertion_trace([5, 2, 5, -1]), separators=(",", ":")))
