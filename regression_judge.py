import json

from ask import looks_like_citation_fragment
from judge import judge
import llm

CHUNKS_FILE = "data/chunks.json"
SCRATCH_CHUNK = "9870175-37"
MAIN_CHUNK = "8623045-1"
JUDGE_CHUNK = "9878807-9"
S, M, J = SCRATCH_CHUNK, MAIN_CHUNK, JUDGE_CHUNK

CASES = [
    ("Clearly established law is defined as the right to be free from unreasonable searches and seizures.", S, False),
    ("A right is clearly established when its contours are sufficiently clear that a reasonable official would understand that his conduct violates it.", M, True),
    ("Whether a right is clearly established is a question of law that only a judge can decide.", J, True),
    ("Qualified immunity protects government officials who are plainly incompetent.", M, False),
    ("Whether a right is clearly established is a question that the jury must decide.", J, False),
    ("Qualified immunity provides no protection to government officials.", S, False),
    ("Qualified immunity would provide no protection if clearly established law were defined as the right to be free from unreasonable searches and seizures.", S, True),
    ("Courts should define clearly established law as the right to be free from unreasonable searches and seizures.", S, False),
    ("When a violation could be made out on a favorable view of the parties' submissions, the next step is to ask whether the right was clearly established.", M, True),
    ("Qualified immunity protects officials who knowingly violate the law.", M, False),
    ("Qualified immunity is meant to protect officials who make reasonable mistakes in the course of duty.", M, True),
    ("Qualified immunity shields an official even if the plaintiff proves a constitutional violation of a clearly established right.", J, False),
    ("To overcome qualified immunity, a plaintiff must show both a constitutional violation and that the right was clearly established.", J, True),
    ("Punitive damages may be awarded in breach of contract cases involving fraud.", "7007101-180", False),
    ("Punitive damages are traditionally unavailable for breach of contract.", "7007101-22", False),
    ("The First Amendment standard for student speech in public schools is the Hazelwood standard, requiring limits be reasonably related to legitimate pedagogical concerns.", "8684153-2", False),
]

def load_chunk_texts():
    """Map chunk_id to chunk text from CHUNKS_FILE."""
    with open(CHUNKS_FILE, encoding="utf-8") as f:
        return {c["chunk_id"]: c["text"] for c in json.load(f)}


def run_regression():
    """Run every case through the judge; print each result and return the number correct."""
    by_id = load_chunk_texts()
    print(f"provider: {llm.PROVIDER}\n")

    print("warming up the model (the first call can take a couple of minutes)...")
    judge(CASES[0][0], by_id[CASES[0][1]])
    print("model is warm\n")

    correct = 0
    for i, (statement, chunk_id, should_pass) in enumerate(CASES, 1):
        print(f"running case {i} of {len(CASES)}...", flush=True)
        label, quote = judge(statement, by_id[chunk_id])
        ok = (label == "ASSERTS") == should_pass
        correct += ok
        print(f"{'OK  ' if ok else 'MISS'} | {label:<22} | should pass: {str(should_pass):<5} | {statement[:55]}")
        if not ok:
            print(f"       judge copied: {quote}")

    print(f"\ncorrect: {correct} of {len(CASES)}")
    return correct


if __name__ == "__main__":
    run_regression()