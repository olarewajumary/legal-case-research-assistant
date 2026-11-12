import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVAL_CASES_FILE = os.path.join(PROJECT_ROOT, "eval_cases.json")
EXPECTED_CASES = 19
EXPECTED_REFUSALS = 8
EXPECTED_KEYS = ["expected_opinion_id", "expected_warning", "id", "question"]

with open(EVAL_CASES_FILE, encoding="utf-8") as f:
    cases = json.load(f)

assert len(cases) == EXPECTED_CASES, f"expected {EXPECTED_CASES} cases, got {len(cases)}"

refusals = 0
for position, case in enumerate(cases, 1):
    assert sorted(case.keys()) == EXPECTED_KEYS, f"case {position}: wrong keys {sorted(case.keys())}"
    assert case["id"] == position, f"case {position}: id is {case['id']}"
    assert isinstance(case["question"], str) and case["question"], f"case {position}: bad question"
    if case["expected_opinion_id"] is None:
        assert case["expected_warning"] is None, f"case {position}: refusal must have no warning"
        refusals += 1
    else:
        assert isinstance(case["expected_opinion_id"], str) and case["expected_opinion_id"], f"case {position}: bad opinion id"
        assert isinstance(case["expected_warning"], bool), f"case {position}: warning must be a bool"

assert refusals == EXPECTED_REFUSALS, f"expected {EXPECTED_REFUSALS} refusals, got {refusals}"
assert len({case["question"] for case in cases}) == EXPECTED_CASES, "duplicate questions"
print("all eval_cases shape checks passed")