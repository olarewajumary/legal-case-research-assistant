import json
import re
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

K = 60


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


with open("data/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)
embeddings = np.load("data/embeddings.npy")
model = SentenceTransformer("all-MiniLM-L6-v2")
bm25 = BM25Okapi([tokenize(c["text"]) for c in chunks])


def rank_positions(scores):
    """Map chunk index -> rank (1 = best)."""
    order = np.argsort(scores)[::-1]
    return {int(i): rank for rank, i in enumerate(order, 1)}


def hybrid_search(query, top_n=5):
    dense_scores = embeddings @ model.encode(query, normalize_embeddings=True)
    bm25_scores = np.array(bm25.get_scores(tokenize(query)))
    dense_rank = rank_positions(dense_scores)
    bm25_rank = rank_positions(bm25_scores)
    fused = {i: 1 / (K + dense_rank[i]) + 1 / (K + bm25_rank[i]) for i in range(len(chunks))}
    top = sorted(fused, key=fused.get, reverse=True)[:top_n]
    return [(i, fused[i], dense_rank[i], bm25_rank[i]) for i in top]


if __name__ == "__main__":
    queries = [
        "Michigan v. Tyler",
        "Can police enter a home without a warrant in an emergency?",
        "What is the recipe for chocolate chip cookies?",
    ]
    for q in queries:
        print(f"\nQUESTION: {q}")
        for i, score, d, b in hybrid_search(q):
            c = chunks[i]
            print(f"  rrf {score:.4f} | dense #{d:<3} | bm25 #{b:<3} | {c['case_name'][:25]} | {c['text'][:70]}")