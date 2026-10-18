import re
from answer import answer


def squash(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


question = "What does clearly established law mean for qualified immunity?"
out = answer(question)
sources = out["sources"]
squashed = [squash(c["text"]) for c in sources]

print("ANSWER:\n", out["answer"], "\n")

quotes = re.findall(r"[“\"]([^”\"]{4,}?)[”\"]", out["answer"])
print("quoted phrases:", len(quotes))
for q in quotes:
    where = [n for n, s in enumerate(squashed, 1) if squash(q) in s]
    status = f"FOUND in source {where}" if where else "NOT FOUND"
    print(f"  {status} | {q}")

cited = sorted({int(n) for n in re.findall(r"[\[【](\d+)[\]】]", out["answer"])})
print("\ncitation numbers used:", cited, "| sources given:", list(range(1, len(sources) + 1)))

print("\n=== SOURCES ===")
for n, c in enumerate(sources, 1):
    print(f"\n[{n}] {c['case_name']} | {c['chunk_id']}")
    print(c["text"])