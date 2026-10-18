import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from limiter import allow_request

WINDOW = 60
LIMIT = 3
HISTORY = [100, 110, 120]

assert allow_request([], 130, LIMIT, WINDOW) is True, "empty history should be allowed"
assert allow_request(HISTORY, 130, LIMIT, WINDOW) is False, "limit reached inside the window"
assert allow_request(HISTORY, 170, LIMIT, WINDOW) is True, "old requests should drop out"
assert allow_request(HISTORY, 181, LIMIT, WINDOW) is True, "all requests expired"
assert allow_request([], 130, 0, WINDOW) is False, "a limit of zero blocks everything"
print("all allow_request checks passed")