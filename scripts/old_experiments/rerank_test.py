from sentence_transformers import CrossEncoder
from hybrid_search import hybrid_search, chunks

ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

queries = [
    "Can police enter a home without a warrant in an emergency?",
    "What does clearly established law mean for qualified immunity?",
    "What is the recipe for chocolate chip cookies?",
]

for q in queries:
    candidates = hybrid_search(q, top_n=10)
    pairs = [(q, chunks[i]["text"]) for i, *_ in candidates]
    scores = ce.predict(pairs)
    ranked = sorted(zip(range(1, 11), candidates, scores), key=lambda x: x[2], reverse=True)
    print(f"\nQUESTION: {q}")
    for fused_pos, (i, rrf, d, b), s in ranked[:4]:
        print(f"  ce {s:7.2f} | was fused #{fused_pos:<2} | {chunks[i]['case_name'][:22]} | {chunks[i]['text'][:70]}")