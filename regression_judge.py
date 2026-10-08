from judge import judge
import json

with open("data/chunks.json", encoding="utf-8") as f:
    by_id = {c["chunk_id"]: c["text"] for c in json.load(f)}

S, M, J = "9870175-37", "8623045-1", "9878807-9"
cases = [
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
]

correct = 0
for statement, chunk_id, should_pass in cases:
    label, _ = judge(statement, by_id[chunk_id])
    ok = (label == "ASSERTS") == should_pass
    correct += ok
    print(f"{'OK  ' if ok else 'MISS'} | {label:<22} | should pass: {str(should_pass):<5} | {statement[:55]}")

print(f"\ncorrect: {correct} of {len(cases)}")