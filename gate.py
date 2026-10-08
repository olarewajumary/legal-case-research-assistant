from sentence_transformers import CrossEncoder
from hybrid_search import hybrid_search, chunks

ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

THRESHOLD = 0.0
REFUSAL = "No relevant precedent found."


def retrieve(query, candidates_n=10, keep=3):
    """Return the best chunks, or a refusal if nothing clears the threshold."""
    candidates = hybrid_search(query, top_n=candidates_n)
    scores = ce.predict([(query, chunks[i]["text"]) for i, *_ in candidates])
    ranked = sorted(zip([c[0] for c in candidates], scores), key=lambda x: x[1], reverse=True)

    best = float(ranked[0][1])
    passing = [(i, float(s)) for i, s in ranked if s >= THRESHOLD][:keep]
    if not passing:
        return {"answerable": False, "best_score": best, "message": REFUSAL, "chunks": []}
    return {"answerable": True, "best_score": best, "message": None, "chunks": passing}


if __name__ == "__main__":
    tests = [
        "Do government officials get immunity when the law was not clearly established?",
        "Can police search a car without a warrant?",
        "Can a prisoner sue for retaliation in the Second Circuit?",
        "What is qualified immunity for firefighters?",
        "What is the First Amendment standard for student speech in public schools?",
        "What damages can a plaintiff recover in a breach of contract case?",
    ]
    for q in tests:
        result = retrieve(q)
        verdict = "ANSWER " if result["answerable"] else "REFUSE "
        print(f"{verdict}| best {result['best_score']:6.2f} | {q}")
        for i, s in result["chunks"][:1]:
            print(f"          top chunk: {chunks[i]['case_name'][:30]} | {chunks[i]['text'][:70]}")