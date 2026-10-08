from gate import retrieve, chunks

questions = [
    ("A", "Can a county be held responsible for a bad policy followed by its social workers?"),
    ("A", "What happens if it's unclear how the jury decided the facts behind qualified immunity?"),
    ("A", "Can someone win a civil rights case but only get one dollar in damages?"),
    ("A", "Does video footage of an incident change whether a case goes to trial?"),
    ("N", "Can police use a drone to look into a backyard without a warrant?"),
    ("N", "Can a government worker be fired for criticizing their boss on social media?"),
    ("N", "What does a police officer need to put in an application for a search warrant?"),
    ("N", "Is a private company responsible under the Constitution for what its employees do?"),
]

mismatches = 0
for label, q in questions:
    result = retrieve(q)
    verdict = "ANSWER" if result["answerable"] else "REFUSE"
    expected = "ANSWER" if label == "A" else "REFUSE"
    flag = "" if verdict == expected else "   <-- MISMATCH"
    mismatches += verdict != expected
    print(f"{label} -> {verdict} | best {result['best_score']:6.2f} | {q}{flag}")
    for i, s in result["chunks"][:1]:
        print(f"      top chunk: {chunks[i]['case_name'][:30]} | {chunks[i]['text'][:100]}")

print(f"\nmismatches: {mismatches} of {len(questions)}")