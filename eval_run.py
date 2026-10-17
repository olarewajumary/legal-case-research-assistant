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