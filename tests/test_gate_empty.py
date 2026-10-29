import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gate


def no_candidates(query, top_n):
    """Stand-in for hybrid_search that finds nothing."""
    return []


real_search = gate.hybrid_search
gate.hybrid_search = no_candidates
try:
    result = gate.retrieve("anything at all")
finally:
    gate.hybrid_search = real_search

assert result["answerable"] is False, "empty candidates should refuse"
assert result["chunks"] == [], "empty candidates should return no chunks"
assert result["message"] == gate.REFUSAL, "empty candidates should use the refusal message"
print("empty candidate check passed")