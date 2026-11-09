import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ask

QUOTE = "the rule is clear"
SOURCE = {
    "text": "The court held that the rule is clear.",
    "case_name": "Test v. Case",
    "court_id": "ca9",
    "date_filed": "2020-01-01",
    "url": "https://example.com/opinion/1/",
    "unpublished": False,
    "opinion_id": 123,
}
CLAIM = {"statement": "The rule is clear.", "source": 1}


def fake_judge(statement, text):
    """Stand-in for the judge: always says ASSERTS with a quote from the source."""
    return "ASSERTS", f"QUOTE: {QUOTE} LABEL: ASSERTS"


real_judge = ask.judge
ask.judge = fake_judge
try:
    kept = ask.verify_claims([SOURCE], [CLAIM])
finally:
    ask.judge = real_judge

assert len(kept) == 1, "the claim should be kept"
assert kept[0].get("opinion_id") == "123", "kept claim should carry opinion_id as a string"
print("opinion_id check passed")