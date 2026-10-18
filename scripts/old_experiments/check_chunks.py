import json
import os
import re
from text_extract import extract_paragraphs
from chunker import chunk_paragraphs, MAX_CHARS

RAW_DIR = os.path.join("data", "raw")


def squash(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


ABBREV_END = re.compile(r"\b(U\.S|Cir|v|No|Inc|Co|Corp|Ct|Id|F\.\dd|F\.\d|Cal|Mr|Dr)\.$")

for name in sorted(os.listdir(RAW_DIR)):
    with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
        rec = json.load(f)
    paras = extract_paragraphs(rec["text"])
    chunks = chunk_paragraphs(paras)

    preserved = squash(" ".join(paras)) == squash(" ".join(chunks))
    over = sum(1 for p in paras if len(p) > MAX_CHARS)
    print(f"{rec['opinion_id']:>9} | text preserved: {preserved} | paragraphs over limit: {over}")

    for c in chunks:
        if ABBREV_END.search(c):
            print("    suspicious chunk end:", repr(c[-60:]))