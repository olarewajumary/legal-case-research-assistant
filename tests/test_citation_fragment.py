import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ask import looks_like_citation_fragment

HASLIP = (
    "Co. v. Haslip, 499 U.S. 1, 6-7 , 111 S.Ct. 1032 , "
    "113 L.Ed.2d 1 (1991) (affirming a punitive damage award);"
)
NORMAL = (
    "The contours of the right must be sufficiently clear that a reasonable "
    "official would understand that what he is doing violates that right."
)
ONE_MARKER = (
    "The Court explained this in Anderson, 483 U.S. 635, 640 (1987), "
    "and the rule is clear."
)

assert looks_like_citation_fragment(HASLIP) is True, "Haslip fragment should be caught"
assert looks_like_citation_fragment(NORMAL) is False, "plain sentence should be kept"
assert looks_like_citation_fragment(ONE_MARKER) is False, "one reporter marker should be kept"
assert looks_like_citation_fragment("") is False, "empty text should be kept"
print("all citation fragment checks passed")