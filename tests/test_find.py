import sys
sys.path.insert(0, ".")
from answer_v2 import find_in_source

text = "Qualified immunity shields officials unless a plaintiff shows a violation."
print(repr(find_in_source("unlessa plaintiff shows", text)))
print(repr(find_in_source("not in the text at all", text)))
print(repr(find_in_source("2) maintenance applies", "The rule is (2) maintenance applies; next.")))