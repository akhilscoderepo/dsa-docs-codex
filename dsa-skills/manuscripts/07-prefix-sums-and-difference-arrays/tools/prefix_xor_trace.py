import json


def build_trace(values, left, right):
    prefix = [0]
    steps = []
    current = 0
    for index, value in enumerate(values):
        current ^= value
        prefix.append(current)
        steps.append({
            "at": {"i": index},
            "vars": {"value": value, "prefixXor": current},
            "note": f"Include index {index}; the boundary after it now stores XOR {current}.",
        })
    answer = prefix[right + 1] ^ prefix[left]
    steps.append({
        "at": {"left": left, "right": right},
        "vars": {
            "prefixAfterRight": prefix[right + 1],
            "prefixBeforeLeft": prefix[left],
            "answer": answer,
        },
        "note": "XOR the two boundary states; the shared prefix cancels.",
    })
    return {"cells": values, "pointers": ["i", "left", "right"], "steps": steps}


if __name__ == "__main__":
    print(json.dumps(build_trace([5, 1, 7, 3], 1, 3), separators=(",", ":")))
