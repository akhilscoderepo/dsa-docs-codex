"""Compute the grouping trace and the representative-scan cost."""
import json
import re
import sys
from pathlib import Path


def trace():
    words = ["pots", "stop", "dog", "tops", "pots", "", ""]
    groups, steps = {}, []
    for i, word in enumerate(words):
        key = "".join(sorted(word))
        created = key not in groups
        groups.setdefault(key, []).append(word)
        steps.append({
            "at": {"scan": i, "group": list(groups).index(key)},
            "vars": {"signature": key, "members": list(groups[key]), "groups": len(groups)},
            "note": f"{word!r} {'creates a group' if created else 'joins an existing group'} under key {key!r}."
        })
    assert list(groups.values()) == [["pots", "stop", "tops", "pots"], ["dog"], ["", ""]]
    representatives = []
    comparisons = visits = 0
    for word in ["aa", "ab", "ac", "ad"]:
        for other in representatives:
            comparisons += 1
            counts = [0] * 26
            for a, b in zip(word, other):
                counts[ord(a) - ord('a')] += 1
                counts[ord(b) - ord('a')] -= 1
                visits += 2
            if all(value == 0 for value in counts):
                break
        else:
            representatives.append(word)
    assert (comparisons, visits) == (6, 24)
    return {"cells": words, "pointers": ["scan", "group"], "steps": steps}


if __name__ == "__main__":
    payload = json.dumps(trace(), separators=(",", ":"))
    if "--update" in sys.argv:
        manuscript = Path(__file__).resolve().parents[1] / "09-strings-maps-and-sorting.md"
        text = manuscript.read_text(encoding="utf-8")
        text, count = re.subn(r"```trace\n.*?\n```", "```trace\n" + payload + "\n```", text, flags=re.S)
        assert count == 1
        manuscript.write_text(text, encoding="utf-8")
    else:
        print(payload)
