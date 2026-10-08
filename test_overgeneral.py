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

cases = [
    ("Qualified immunity protects all government officials from suit.",
     "8623045-1", "clear overgeneralization: source says 'all but the plainly incompetent or those who knowingly violate the law'"),
    ("Qualified immunity protects government officials who make reasonable mistakes in the course of duty.",
     "8623045-1", "faithful: ASSERTS"),
    ("Juries never decide any part of a qualified immunity case.",
     "9878807-9", "overgeneral: source only says the clearly established inquiry is for a judge"),
    ("Whether a right is clearly established is a question of law.",
     "9878807-9", "narrower than the source, still true: ASSERTS"),
    ("Courts must reject any definition of clearly established law that is as broad as the right to be free from unreasonable searches and seizures.",
     "9870175-37", "debatable, my reading only"),
]

for statement, chunk_id, expectation in cases:
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
    print(f"{label:<22} | {expectation}\n   {statement[:90]}")