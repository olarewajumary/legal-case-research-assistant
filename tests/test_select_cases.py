import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval_run import select_cases

CASES = [{"id": 1}, {"id": 2}, {"id": 12}]

assert select_cases(CASES, []) == CASES, "no ids should return every case"
assert select_cases(CASES, [12]) == [{"id": 12}], "one id should return one case"
assert select_cases(CASES, [2, 1]) == [{"id": 1}, {"id": 2}], "keeps file order"
assert select_cases(CASES, [99]) == [], "unknown id should return nothing"
print("all select_cases checks passed")