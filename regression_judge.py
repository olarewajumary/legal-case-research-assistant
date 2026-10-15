from judge import judge
import json
import llm

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
    ("Punitive damages may be awarded in breach of contract cases involving fraud.", "7007101-180", False),
]

print(f"provider: {llm.PROVIDER}\n")

print("warming up the model (the first call can take a couple of minutes)...")
judge(cases[0][0], by_id[cases[0][1]])
print("model is warm\n")

correct = 0
for i, (statement, chunk_id, should_pass) in enumerate(cases, 1):
    print(f"running case {i} of {len(cases)}...", flush=True)
    label, quote = judge(statement, by_id[chunk_id])
    ok = (label == "ASSERTS") == should_pass
    correct += ok
    print(f"{'OK  ' if ok else 'MISS'} | {label:<22} | should pass: {str(should_pass):<5} | {statement[:55]}")
    
    if not ok:
        print(f"       judge copied: {quote}")
        
print(f"\ncorrect: {correct} of {len(cases)}")

from ask import looks_like_citation_fragment

print("citation fragment caught:", looks_like_citation_fragment(
    "Co. v. Haslip, 499 U.S. 1, 6-7 , 111 S.Ct. 1032 , 113 L.Ed.2d 1 (1991) (affirming a punitive damage award);"))
print("normal sentence kept:", not looks_like_citation_fragment(
    "The contours of the right must be sufficiently clear that a reasonable official would understand that what he is doing violates that right."))