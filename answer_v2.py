import json
import os
import re
from dotenv import load_dotenv
from gate import retrieve, chunks
from llm import chat

load_dotenv()

SYSTEM = (
    "You are a legal research assistant. Answer using ONLY the numbered sources provided. "
    "Return ONLY a JSON object, with no other text, in this shape: "
    '{"claims": [{"statement": "...", "source": 1, "quote": "..."}]} '
    "Each claim is one short statement. 'source' is the number of the source that supports it. "
    "'quote' is a verbatim passage of at most 25 words from that source. "
    "Only make a claim that the source itself states. If a source warns against or criticizes a "
    "proposition, do not present that proposition as the rule. "
    'If the sources do not answer the question, return {"claims": []}. '
    "Do not use outside knowledge and do not invent cases or citations."
)


def squash(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def get_claims(question):
    result = retrieve(question)
    if not result["answerable"]:
        return None, []

    sources = [chunks[i] for i, _ in result["chunks"]]
    context = "\n\n".join(
        f"[{n}] {c['case_name']} ({c['court_id']}, filed {c['date_filed']})\n{c['text']}"
        for n, c in enumerate(sources, 1)
    )
    raw, finish_reason, _ = chat(
        [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Sources:\n\n{context}\n\nQuestion: {question}"},
        ],
        role="writer",
    )
    if finish_reason != "stop":
        print("WARNING: finish reason was", finish_reason)

    start, end = raw.find("{"), raw.rfind("}")
    try:
        claims = json.loads(raw[start:end + 1])["claims"]
    except Exception as e:
        print("COULD NOT PARSE JSON:", type(e).__name__)
        print(raw[:500])
        return sources, []
    return sources, claims


if __name__ == "__main__":
    question = "What does clearly established law mean for qualified immunity?"
    sources, claims = get_claims(question)
    print("claims parsed:", len(claims))
    for c in claims:
        n = c.get("source")
        valid = isinstance(n, int) and 1 <= n <= len(sources)
        found = valid and squash(c.get("quote", "")) in squash(sources[n - 1]["text"])
        print(f"\n[{n}] {'quote found' if found else 'QUOTE NOT FOUND OR BAD SOURCE NUMBER'}")
        print("  statement:", c.get("statement"))
        print("  quote:    ", c.get("quote"))