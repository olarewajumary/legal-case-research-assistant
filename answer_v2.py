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


OPENERS = "(\u201c\u2018\"'["
CLOSERS = ".;,:)\u201d\u2019\"'?]"


def find_in_source(quote, text):
    """Return the exact slice of text that matches quote, ignoring spacing and punctuation; None if absent."""
    wanted = squash(quote)
    if not wanted:
        return None
    kept = []  # (character, index in original text) for each letter or digit
    for i, ch in enumerate(text):
        if re.match(r"[A-Za-z0-9]", ch):
            kept.append((ch.lower(), i))
    flat = "".join(ch for ch, _ in kept)
    start = flat.find(wanted)
    if start == -1:
        return None
    first = kept[start][1]
    last = kept[start + len(wanted) - 1][1]
    while first > 0 and text[first - 1] in OPENERS:
        first -= 1
    while last + 1 < len(text) and text[last + 1] in CLOSERS:
        last += 1
    return text[first:last + 1]


def parse_claims(raw):
    """Return the list of claims from the writer's reply, or None if the reply is broken."""
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(raw[start:end + 1])["claims"]
    except (ValueError, KeyError, TypeError):
        return None


def get_claims(question):
    """Retrieve sources, ask the writer for claims, and return (sources, claims)."""
    result = retrieve(question)
    if not result["answerable"]:
        return None, []

    sources = [chunks[i] for i, _ in result["chunks"]]
    context = "\n\n".join(
        f"[{n}] {c['case_name']} ({c['court_id']}, filed {c['date_filed']})\n{c['text']}"
        for n, c in enumerate(sources, 1)
    )
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Sources:\n\n{context}\n\nQuestion: {question}"},
    ]
    raw, finish_reason, _ = chat(messages, role="writer")
    if finish_reason != "stop":
        print("WARNING: finish reason was", finish_reason)

    claims = parse_claims(raw)
    if claims is None:
        print("COULD NOT PARSE JSON, retrying once")
        print(raw[:500])
        raw, finish_reason, _ = chat(messages, role="writer")
        claims = parse_claims(raw)
        if claims is None:
            print("RETRY ALSO FAILED")
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