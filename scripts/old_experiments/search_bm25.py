import json
import re
from rank_bm25 import BM25Okapi


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


with open("data/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

bm25 = BM25Okapi([tokenize(c["text"]) for c in chunks])

queries = [
    "Michigan v. Tyler",
    "Can police enter a home without a warrant in an emergency?",
    "What is the recipe for chocolate chip cookies?",
]

for q in queries:
    scores = bm25.get_scores(tokenize(q))
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:3]
    print(f"\nQUESTION: {q}")
    for rank, i in enumerate(top, 1):
        c = chunks[i]
        print(f"  {rank}. score {scores[i]:.2f} | {c['case_name'][:35]} | {c['text'][:90]}")