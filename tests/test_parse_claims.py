import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from answer_v2 import parse_claims

GOOD = '{"claims": [{"statement": "a", "source": 1}]}'
EMPTY = '{"claims": []}'
BROKEN_BRACKETS = '{"claims": [{"statement": "a", "source": 1}]]}'
NO_JSON = "Sorry, I cannot answer that."
WRAPPED = 'Here you go: {"claims": []} thanks'

assert len(parse_claims(GOOD)) == 1, "good reply should give 1 claim"
assert parse_claims(EMPTY) == [], "empty claims should be [], not None"
assert parse_claims(BROKEN_BRACKETS) is None, "broken brackets should be None"
assert parse_claims(NO_JSON) is None, "no JSON should be None"
assert parse_claims(WRAPPED) == [], "JSON inside extra text should still parse"
print("all parse_claims checks passed")