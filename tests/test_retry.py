import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import answer_v2

GOOD = '{"claims": [{"statement": "a", "source": 1}]}'
BROKEN = '{"claims": [{"statement": "a", "source": 1}]]}'
QUESTION = "What are the factors for a stay pending appeal?"


def run_with_replies(replies):
    """Run get_claims with chat faked to return the given replies in order."""
    calls = []

    def fake_chat(messages, role):
        calls.append(role)
        return replies[len(calls) - 1], "stop", None

    real_chat = answer_v2.chat
    answer_v2.chat = fake_chat
    try:
        sources, claims = answer_v2.get_claims(QUESTION)
    finally:
        answer_v2.chat = real_chat
    return claims, len(calls)


claims, calls = run_with_replies([GOOD])
assert len(claims) == 1 and calls == 1, "good reply: 1 claim, no retry"

claims, calls = run_with_replies([BROKEN, GOOD])
assert len(claims) == 1 and calls == 2, "broken then good: 1 claim, 2 calls"

claims, calls = run_with_replies([BROKEN, BROKEN])
assert claims == [] and calls == 2, "broken twice: [], exactly 2 calls"

print("all retry checks passed")