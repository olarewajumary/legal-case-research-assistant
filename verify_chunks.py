import json
import os
import re
from text_extract import extract_paragraphs
from chunker import chunk_paragraphs, MAX_CHARS

RAW_DIR = os.path.join("data", "raw")


def squash(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


preserved_count = 0
total_chunks = 0
biggest = 0
over_limit = 0

for name in sorted(os.listdir(RAW_DIR)):
    with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
        rec = json.load(f)
    paras = extract_paragraphs(rec["text"])
    chunks = chunk_paragraphs(paras)

    if squash(" ".join(paras)) == squash(" ".join(chunks)):
        preserved_count += 1
    else:
        print("TEXT LOST OR DUPLICATED:", name)

    total_chunks += len(chunks)
    biggest = max(biggest, max(len(c) for c in chunks))
    over_limit += sum(1 for c in chunks if len(c) > MAX_CHARS)

print("opinions with text preserved:", preserved_count, "of 10")
print("total chunks:", total_chunks)
print("biggest chunk (chars):", biggest)
print("chunks over", MAX_CHARS, "chars:", over_limit)