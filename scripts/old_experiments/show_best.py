from sentence_transformers import CrossEncoder
from hybrid_search import hybrid_search, chunks

ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
q = "Does video footage of an incident change whether a case goes to trial?"

candidates = hybrid_search(q, top_n=10)
scores = ce.predict([(q, chunks[i]["text"]) for i, *_ in candidates])
ranked = sorted(zip([c[0] for c in candidates], scores), key=lambda x: x[1], reverse=True)

for i, s in ranked[:3]:
    print(f"--- score {s:.2f} | {chunks[i]['case_name'][:30]}")
    print(chunks[i]["text"])
    print()