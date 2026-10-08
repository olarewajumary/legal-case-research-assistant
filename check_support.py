import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL")

with open("data/chunks.json", encoding="utf-8") as f:
    by_id = {c["chunk_id"]: c["text"] for c in json.load(f)}

JUDGE = (
    "You check whether a source passage supports a statement. "
    "Reply with SUPPORTED or NOT_SUPPORTED as the first word, then one short sentence of reasoning. "
    "Answer NOT_SUPPORTED if the passage says the opposite, mentions the statement only as "
    "something to avoid or criticize, or does not actually state it."
)

cases = [
    ("Clearly established law is defined as the right to be free from unreasonable searches and seizures.",
     "9870175-37", "NOT_SUPPORTED"),
    ("A right is clearly established when its contours are sufficiently clear that a reasonable official would understand that his conduct violates it.",
     "8623045-1", "SUPPORTED"),
    ("Whether a right is clearly established is a question of law that only a judge can decide.",
     "9878807-9", "SUPPORTED"),
]

for statement, chunk_id, expected in cases:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": JUDGE},
            {"role": "user", "content": f"Passage:\n{by_id[chunk_id]}\n\nStatement: {statement}"},
        ],
        temperature=0,
    )
    choice = response.choices[0]
    verdict = choice.message.content.strip()
    first = verdict.split()[0].strip(".,:").upper() if verdict else "EMPTY"
    flag = "" if first == expected else "   <-- UNEXPECTED"
    print(f"expected {expected} | got: {verdict[:160]}{flag}")
    if choice.finish_reason != "stop":
        print("   WARNING: finish reason", choice.finish_reason)