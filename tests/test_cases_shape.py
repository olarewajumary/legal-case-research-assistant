import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from regression_judge import CASES, CHUNKS_FILE

EXPECTED_CASES = 15

with open(CHUNKS_FILE, encoding="utf-8") as f:
    chunk_ids = {c["chunk_id"] for c in json.load(f)}

assert len(CASES) == EXPECTED_CASES, f"expected {EXPECTED_CASES} cases, got {len(CASES)}"
for i, (statement, chunk_id, should_pass) in enumerate(CASES, 1):
    assert isinstance(statement, str) and statement, f"case {i}: bad statement"
    assert chunk_id in chunk_ids, f"case {i}: chunk {chunk_id} not in chunks file"
    assert isinstance(should_pass, bool), f"case {i}: should_pass must be a bool"
assert len({case[0] for case in CASES}) == EXPECTED_CASES, "duplicate statements"
print("all CASES shape checks passed")