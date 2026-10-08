import re
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

    if valid:
        label, raw = judge(c.get("statement", ""), passage)
        match = re.search(r"QUOTE:\s*(.*?)\s*LABEL:", raw, re.DOTALL)
        judge_quote = match.group(1).strip() if match else ""
    else:
        label, judge_quote = "BAD_SOURCE", ""

    quote_real = bool(judge_quote) and squash(judge_quote) in squash(passage)
    keep = label == "ASSERTS" and quote_real
    kept += keep

    print(f"\n{'KEEP' if keep else 'DROP'} | judge: {label} | judge quote real: {quote_real}")
    print("  statement:", c.get("statement"))
    if keep:
        print(f"  cite: [{n}] {sources[n - 1]['case_name']}")
        print("  quote:", judge_quote)

print(f"\nkept {kept} of {len(claims)} claims")