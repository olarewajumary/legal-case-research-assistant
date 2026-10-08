from answer_v2 import get_claims, squash
from judge import judge

question = "What does clearly established law mean for qualified immunity?"
sources, claims = get_claims(question)

print("claims:", len(claims))
kept = 0
for c in claims:
    n = c.get("source")
    valid = isinstance(n, int) and sources is not None and 1 <= n <= len(sources)
    passage = sources[n - 1]["text"] if valid else ""
    quote_ok = valid and squash(c.get("quote", "")) in squash(passage)
    label = judge(c.get("statement", ""), passage)[0] if valid else "BAD_SOURCE"
    keep = quote_ok and label == "ASSERTS"
    kept += keep
    print(f"\n{'KEEP' if keep else 'DROP'} | quote found: {quote_ok} | judge: {label}")
    print("  ", c.get("statement"))

print(f"\nkept {kept} of {len(claims)} claims")