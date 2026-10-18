import json
import os
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODELS = ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b"]

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
    ("Qualified immunity provides no protection to government officials.",
     "9870175-37", False),
    ("Qualified immunity would provide no protection if clearly established law were defined as the right to be free from unreasonable searches and seizures.",
     "9870175-37", True),
    ("Courts should define clearly established law as the right to be free from unreasonable searches and seizures.",
     "9870175-37", False),
    ("When a violation could be made out on a favorable view of the parties' submissions, the next step is to ask whether the right was clearly established.",
     "8623045-1", True),
    ("Qualified immunity protects officials who knowingly violate the law.",
     "8623045-1", False),
    ("Qualified immunity is meant to protect officials who make reasonable mistakes in the course of duty.",
     "8623045-1", True),
    ("Qualified immunity shields an official even if the plaintiff proves a constitutional violation of a clearly established right.",
     "9878807-9", False),
    ("To overcome qualified immunity, a plaintiff must show both a constitutional violation and that the right was clearly established.",
     "9878807-9", True),
]

for model in MODELS:
    print(f"\n===== {model} =====")
    correct = 0
    for statement, chunk_id, should_pass in cases:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": JUDGE},
                    {"role": "user", "content": f"Passage:\n{by_id[chunk_id]}\n\nStatement: {statement}"},
                ],
                temperature=0,
            )
        except Exception as e:
            print("FAILED:", type(e).__name__, "-", str(e)[:150])
            break
        choice = response.choices[0]
        text = choice.message.content or ""
        match = re.search(r"LABEL:\s*([A-Z_]+)", text)
        label = match.group(1) if match else "UNPARSED"
        ok = (label == "ASSERTS") == should_pass
        correct += ok
        print(f"{'OK  ' if ok else 'MISS'} | {label:<22} | should pass: {str(should_pass):<5} | {statement[:50]}")
        if choice.finish_reason != "stop":
            print("       WARNING: finish reason", choice.finish_reason)
    else:
        print(f"correct: {correct} of {len(cases)}")