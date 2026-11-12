import sys

sys.path.insert(0, ".")

from answer_v2 import find_in_source

TEXT = "Qualified immunity shields officials unless a plaintiff shows a violation."
NUMBERED_TEXT = "The rule is (2) maintenance applies; next."

result_found = find_in_source("unlessa plaintiff shows", TEXT)
assert result_found == "unless a plaintiff shows", result_found

result_missing = find_in_source("not in the text at all", TEXT)
assert result_missing is None, result_missing

result_numbered = find_in_source("2) maintenance applies", NUMBERED_TEXT)
assert result_numbered == "(2) maintenance applies;", result_numbered

print("test_find: all 3 checks passed")