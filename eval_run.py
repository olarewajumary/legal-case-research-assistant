import json
import sys
from collections import Counter

from ask import ask

STATUS_ANSWERED = "answered"
STATUS_REFUSED = "refused"

CORRECT_REFUSAL = "correct refusal"
NOT_REFUSED = "not refused"
WRONGLY_REFUSED = "wrongly refused"
UNVERIFIED = "unverified"
WRONG_CASE = "wrong case"
WARNING_MISMATCH = "warning mismatch"
CASE_MATCH = "case match"


def score_case(case, out):
    """Score one ask() result against one case; judges only the first claim."""
    if case["expected_opinion_id"] is None:
        if out["status"] == STATUS_REFUSED:
            return CORRECT_REFUSAL
        return NOT_REFUSED
    if out["status"] == STATUS_REFUSED:
        return WRONGLY_REFUSED
    if out["status"] != STATUS_ANSWERED:
        return UNVERIFIED
    first = out["claims"][0]
    if first["opinion_id"] != case["expected_opinion_id"]:
        return WRONG_CASE
    if first["unpublished"] != case["expected_warning"]:
        return WARNING_MISMATCH
    return CASE_MATCH


CASES_FILE = "eval_cases.json"
DEFAULT_RUNS = 1


def load_cases():
    """Read the evaluation cases from CASES_FILE."""
    with open(CASES_FILE, encoding="utf-8") as f:
        return json.load(f)


def select_cases(cases, ids):
    """Return the cases whose id is in ids, in file order; all cases if ids is empty."""
    if not ids:
        return cases
    return [case for case in cases if case["id"] in ids]


def run_all(runs, ids):
    """Run the selected cases `runs` times; print one line per run and a tally."""
    tally = Counter()
    for case in select_cases(load_cases(), ids):
        for i in range(runs):
            label = score_case(case, ask(case["question"]))
            tally[label] += 1
            print(f"Q{case['id']} run {i + 1}: {label}")
    print("\nTally:")
    for label, count in sorted(tally.items()):
        print(f"  {label}: {count}")

if __name__ == "__main__":
    args = [int(arg) for arg in sys.argv[1:]]
    run_count = args[0] if args else DEFAULT_RUNS
    run_all(run_count, args[1:])