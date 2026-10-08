import json
import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
JUDGE_MODEL = os.getenv("GROQ_JUDGE_MODEL")

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


def judge(statement, passage):
    """Return (label, raw_text) for how the passage relates to the statement."""
    response = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[
            {"role": "system", "content": JUDGE},
            {"role": "user", "content": f"Passage:\n{passage}\n\nStatement: {statement}"},
        ],
        temperature=0,
    )
    text = response.choices[0].message.content or ""
    match = re.search(r"LABEL:\s*([A-Z_]+)", text)
    return (match.group(1) if match else "UNPARSED"), text


if __name__ == "__main__":
    with open("data/chunks.json", encoding="utf-8") as f:
        by_id = {c["chunk_id"]: c["text"] for c in json.load(f)}

    print("judge model:", JUDGE_MODEL)
    tests = [
        ("Clearly established law is defined as the right to be free from unreasonable searches and seizures.",
         "9870175-37"),
        ("Whether a right is clearly established is a question of law that only a judge can decide.",
         "9878807-9"),
    ]
    for statement, chunk_id in tests:
        labels = [judge(statement, by_id[chunk_id])[0] for _ in range(5)]
        print(f"\n{statement[:70]}\n  5 runs: {labels}")