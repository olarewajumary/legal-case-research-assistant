import json
import re
from judge import client, JUDGE_MODEL

with open("data/chunks.json", encoding="utf-8") as f:
    by_id = {c["chunk_id"]: c["text"] for c in json.load(f)}

JUDGE_V2 = (
    "You check how a source passage relates to a statement. Respond in exactly two lines.\n"
    "Line 1: QUOTE: <copy, word for word, the single sentence from the passage most relevant to the statement>\n"
    "Line 2: LABEL: <one of the following>\n"
    "  ASSERTS - the passage states the statement, with the same scope and conditions\n"
    "  OVERGENERAL - the passage supports only a narrower version: it applies a rule to specific facts, "
    "or it adds a condition that the statement leaves out\n"
    "  CONTRADICTS - the passage states the opposite\n"
    "  CONDITIONAL_OR_WARNING - the passage mentions the statement only inside an 'if', as a hypothetical, "
    "or as something to avoid or criticize\n"
    "  NOT_STATED - the passage does not address the statement\n"
    "Read the quoted sentence carefully, including words like 'if', 'not', 'no', 'unless', and 'in this case'."
)

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
    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[
            {"role": "system", "content": JUDGE_V2},
            {"role": "user", "content": f"Passage:\n{by_id[chunk_id]}\n\nStatement: {statement}"},
        ],
        temperature=0,
    )
    text = response.choices[0].message.content or ""
    match = re.search(r"LABEL:\s*([A-Z_]+)", text)
    label = match.group(1) if match else "UNPARSED"
    ok = (label == "ASSERTS") == should_pass
    correct += ok
    print(f"{'OK  ' if ok else 'MISS'} | {label:<22} | should pass: {str(should_pass):<5} | {statement[:55]}")

print(f"\ncorrect: {correct} of {len(cases)}")