import json
import numpy as np
from sentence_transformers import SentenceTransformer

with open("data/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)
embeddings = np.load("data/embeddings.npy")
model = SentenceTransformer("all-MiniLM-L6-v2")

queries = [
    "Can police enter a home without a warrant in an emergency?",
    "What is the recipe for chocolate chip cookies?",
]

for q in queries:
    q_vec = model.encode(q, normalize_embeddings=True)
    scores = embeddings @ q_vec
    top = np.argsort(scores)[::-1][:3]
    print(f"\nQUESTION: {q}")
    for rank, i in enumerate(top, 1):
        c = chunks[i]
        print(f"  {rank}. score {scores[i]:.3f} | {c['case_name'][:35]} | {c['text'][:90]}")