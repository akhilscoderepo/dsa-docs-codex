import json
import sys


def exact():
    nums, target = [-8, -1, 4, 9, 13, 21, 34], 13
    lo, hi, steps = 0, len(nums) - 1, []
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        steps.append({"at": {"lo": lo, "mid": mid, "hi": hi}, "vars": {"value": nums[mid]},
                      "note": f"Compare index {mid} with target {target}."})
        if nums[mid] == target:
            break
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return {"cells": nums, "pointers": ["lo", "mid", "hi"], "steps": steps}


def first_last():
    nums, target = [1, 3, 3, 3, 3, 8, 12], 3
    lo, hi, ans, steps = 0, len(nums) - 1, -1, []
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        note = "Keep the match and continue left." if nums[mid] == target else "Move toward the target."
        steps.append({"at": {"lo": lo, "mid": mid, "hi": hi}, "vars": {"candidate": ans}, "note": note})
        if nums[mid] >= target:
            if nums[mid] == target: ans = mid
            hi = mid - 1
        else: lo = mid + 1
    return {"cells": nums, "pointers": ["lo", "mid", "hi"], "steps": steps}


def bounds():
    nums, target = [2, 2, 5, 5, 5, 9], 5
    lo, hi, steps = 0, len(nums), []
    while lo < hi:
        mid = lo + (hi - lo) // 2
        steps.append({"at": {"lo": lo, "mid": mid, "hi": hi}, "vars": {"value": nums[mid]},
                      "note": "Equality still belongs to the possible lower-bound suffix." if nums[mid] >= target else "This position is strictly too small."})
        if nums[mid] >= target: hi = mid
        else: lo = mid + 1
    return {"cells": nums, "pointers": ["lo", "mid", "hi"], "steps": steps}


def first_true():
    cells = [False, False, False, True, True, True]
    lo, hi, steps = 0, len(cells), []
    while lo < hi:
        mid = lo + (hi - lo) // 2
        steps.append({"at": {"lo": lo, "mid": mid, "hi": hi}, "vars": {"predicate": cells[mid]},
                      "note": "A true result keeps mid as a candidate." if cells[mid] else "A false result proves the prefix impossible."})
        if cells[mid]: hi = mid
        else: lo = mid + 1
    return {"cells": cells, "pointers": ["lo", "mid", "hi"], "steps": steps}


def peak():
    nums = [1, 4, 8, 11, 7, 3]
    lo, hi, steps = 0, len(nums) - 1, []
    while lo < hi:
        mid = lo + (hi - lo) // 2
        rising = nums[mid] < nums[mid + 1]
        steps.append({"at": {"lo": lo, "mid": mid, "hi": hi}, "vars": {"rising": rising},
                      "note": "The rising edge keeps a peak to the right." if rising else "The flat-or-falling edge keeps mid and the left side."})
        if rising: lo = mid + 1
        else: hi = mid
    return {"cells": nums, "pointers": ["lo", "mid", "hi"], "steps": steps}


def rotated_min():
    nums = [12, 16, 20, 2, 5, 8]
    lo, hi, steps = 0, len(nums) - 1, []
    while lo < hi:
        mid = lo + (hi - lo) // 2
        steps.append({"at": {"lo": lo, "mid": mid, "hi": hi}, "vars": {"midValue": nums[mid], "rightValue": nums[hi]},
                      "note": "Mid exceeds the right endpoint, so the pivot is strictly right." if nums[mid] > nums[hi] else "Mid may be the minimum, so keep it with the left side."})
        if nums[mid] > nums[hi]: lo = mid + 1
        else: hi = mid
    return {"cells": nums, "pointers": ["lo", "mid", "hi"], "steps": steps}


def rotated_target():
    nums, target = [15, 18, 2, 3, 6, 9, 12], 6
    lo, hi, steps = 0, len(nums) - 1, []
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        steps.append({"at": {"lo": lo, "mid": mid, "hi": hi}, "vars": {"value": nums[mid]},
                      "note": "Identify the sorted half before testing whether the target lies inside it."})
        if nums[mid] == target: break
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]: hi = mid - 1
            else: lo = mid + 1
        elif nums[mid] < target <= nums[hi]: lo = mid + 1
        else: hi = mid - 1
    return {"cells": nums, "pointers": ["lo", "mid", "hi"], "steps": steps}


def integer_answer():
    piles, hours = [11, 7, 5, 19], 9
    lo, hi, steps = 1, max(piles), []
    while lo < hi:
        mid = lo + (hi - lo) // 2
        used = sum((p + mid - 1) // mid for p in piles)
        steps.append({"at": {"lo": lo, "mid": mid, "hi": hi}, "vars": {"hours": used},
                      "note": "Feasible speed; keep it and search slower." if used <= hours else "Too slow; discard this speed and every smaller one."})
        if used <= hours: hi = mid
        else: lo = mid + 1
    return {"cells": piles, "pointers": ["lo", "mid", "hi"], "steps": steps}


def continuous():
    x, lo, hi, steps = 10.0, 0.0, 10.0, []
    for i in range(6):
        mid = (lo + hi) / 2.0
        steps.append({"at": {}, "vars": {"lo": round(lo, 4), "mid": round(mid, 4), "hi": round(hi, 4)},
                      "note": "The square is too large, so keep the left half." if mid * mid > x else "The square is small enough, so keep the right half."})
        if mid * mid > x: hi = mid
        else: lo = mid
    return {"cells": [10.0], "pointers": [], "steps": steps}


MODES = {"exact": exact, "first-last": first_last, "bounds": bounds, "first-true": first_true,
         "peak": peak, "rotated-min": rotated_min, "rotated-target": rotated_target,
         "integer-answer": integer_answer, "continuous": continuous}
print(json.dumps(MODES[sys.argv[1]](), separators=(",", ":")))
