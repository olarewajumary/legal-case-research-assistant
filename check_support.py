import json
import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL")

with open("data/chunks.json", encoding="utf-8") as f:
    by_id = {c["chunk_id"]: c["text"] for c in json.load(f)}

JUDGE = (
    "You check how a source passage relates to a statement. Respond in exactly two lines.\n"
    "Line 1: QUOTE: <copy, word for word, the single sentence from the passage most relevant to the statement>\n"
    "Line 2: LABEL: <one of the following>\n"
    "  ASSERTS - the passage states the statement as true\n"
    "  CONTRADICTS - the passage states the opposite\n"
    "  CONDITIONAL_OR_WARNING - the passage mentions the statement only inside an 'if', as a hypothetical, "
    "or as something to avoid or criticize\n"
    "  NOT_STATED - the passage does not address the statement\n"
    "Read the quoted sentence carefully, including words like 'if', 'not', 'no', and 'unless'."
)

cases = [
    ("Clearly established law is defined as the right to be free from unreasonable searches and seizures.",
     "9870175-37", False),
    ("A right is clearly established when its contours are sufficiently clear that a reasonable official would understand that his conduct violates it.",
     "8623045-1", True),
    ("Whether a right is clearly established is a question of law that only a judge can decide.",
     "9878807-9", True),
    ("Qualified immunity protects government officials who are plainly incompetent.",
     "8623045-1", False),
    ("Whether a right is clearly established is a question that the jury must decide.",
     "9878807-9", False),
]

correct = 0
for statement, chunk_id, should_pass in cases:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": JUDGE},
            {"role": "user", "content": f"Passage:\n{by_id[chunk_id]}\n\nStatement: {statement}"},
        ],
        temperature=0,
    )
    choice = response.choices[0]
    text = choice.message.content or ""
    match = re.search(r"LABEL:\s*([A-Z_]+)", text)
    label = match.group(1) if match else "UNPARSED"
    passed = label == "ASSERTS"
    ok = passed == should_pass
    correct += ok
    print(f"{'OK  ' if ok else 'MISS'} | label {label} | should pass: {should_pass} | {statement[:70]}")
    print("      ", text.replace("\n", " ")[:220])
    if choice.finish_reason != "stop":
        print("       WARNING: finish reason", choice.finish_reason)

print(f"\ncorrect: {correct} of {len(cases)}")