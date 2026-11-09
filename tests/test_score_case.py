import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eval_run import (
    score_case,
    CORRECT_REFUSAL,
    NOT_REFUSED,
    WRONGLY_REFUSED,
    UNVERIFIED,
    WRONG_CASE,
    WARNING_MISMATCH,
    CASE_MATCH,
)

ANSWER_CASE = {"id": 1, "expected_opinion_id": "111", "expected_warning": True}
REFUSAL_CASE = {"id": 4, "expected_opinion_id": None, "expected_warning": None}


def answered(opinion_id, unpublished):
    """Build a fake answered result with one claim."""
    claim = {"opinion_id": opinion_id, "unpublished": unpublished}
    return {"status": "answered", "claims": [claim]}


REFUSED = {"status": "refused", "claims": []}
UNVERIFIED_OUT = {"status": "unverified", "claims": []}

assert score_case(REFUSAL_CASE, REFUSED) == CORRECT_REFUSAL
assert score_case(REFUSAL_CASE, UNVERIFIED_OUT) == NOT_REFUSED
assert score_case(REFUSAL_CASE, answered("111", True)) == NOT_REFUSED
assert score_case(ANSWER_CASE, REFUSED) == WRONGLY_REFUSED
assert score_case(ANSWER_CASE, UNVERIFIED_OUT) == UNVERIFIED
assert score_case(ANSWER_CASE, answered("999", True)) == WRONG_CASE
assert score_case(ANSWER_CASE, answered("111", False)) == WARNING_MISMATCH
assert score_case(ANSWER_CASE, answered("111", True)) == CASE_MATCH
print("all score_case checks passed")