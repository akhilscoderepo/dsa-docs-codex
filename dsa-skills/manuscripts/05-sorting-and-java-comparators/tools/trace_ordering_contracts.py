import json


def selection_trace(values):
    a = values[:]
    steps = []
    comparisons = 0
    for fixed in range(len(a)):
        smallest = fixed
        steps.append({"at": {"fixed": fixed, "scan": fixed}, "vars": {"smallest": a[smallest], "comparisons": comparisons},
                      "note": f"Position {fixed} is unresolved; start with {a[smallest]} as its candidate."})
        for scan in range(fixed + 1, len(a)):
            comparisons += 1
            if a[scan] < a[smallest]:
                smallest = scan
                note = f"Compare index {scan}; {a[scan]} is smaller, so it becomes the candidate."
            else:
                note = f"Compare index {scan}; keep {a[smallest]} as the candidate."
            steps.append({"at": {"fixed": fixed, "scan": scan}, "vars": {"smallest": a[smallest], "comparisons": comparisons}, "note": note})
        a[fixed], a[smallest] = a[smallest], a[fixed]
        steps.append({"at": {"fixed": fixed, "scan": smallest}, "vars": {"smallest": a[fixed], "comparisons": comparisons},
                      "note": f"Place {a[fixed]} at index {fixed}; that prefix now satisfies ascending order."})
    return {"cells": values, "pointers": ["fixed", "scan"], "steps": steps}


if __name__ == "__main__":
    print(json.dumps(selection_trace([7, -2, 7, 3]), separators=(",", ":")))
