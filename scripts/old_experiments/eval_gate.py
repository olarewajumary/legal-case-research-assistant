from sentence_transformers import CrossEncoder
from hybrid_search import hybrid_search, chunks

ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

questions = [
    ("A", "What does clearly established law mean for qualified immunity?"),
    ("A", "Can a prisoner sue for retaliation after filing grievances?"),
    ("A", "When can officers seize a child without a warrant?"),
    ("A", "Can a jury be given a general verdict form in a qualified immunity case?"),
    ("A", "What is deliberate indifference to a prisoner's rights?"),
    ("A", "Can police enter a home without a warrant in an emergency?"),
    ("N", "What is the recipe for chocolate chip cookies?"),
    ("N", "Who won the 2018 World Cup?"),
    ("N", "How does photosynthesis work?"),
    ("N", "What is the statute of limitations for medical malpractice in Ohio?"),
    ("N", "How do I register a trademark for my logo?"),
    ("N", "What are the grounds for divorce in Texas?"),
]

for label, q in questions:
    candidates = hybrid_search(q, top_n=10)
    scores = ce.predict([(q, chunks[i]["text"]) for i, *_ in candidates])
    print(f"{label} | best {max(scores):6.2f} | {q}")