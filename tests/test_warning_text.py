import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ask import UNPUBLISHED_WARNING

assert "summary order" in UNPUBLISHED_WARNING, "should mention summary orders"
assert "unpublished" in UNPUBLISHED_WARNING, "should mention unpublished opinions"
assert "not binding precedent" in UNPUBLISHED_WARNING, "should say not binding precedent"
print("warning text checks passed")