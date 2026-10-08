import json
import os
from text_extract import extract_paragraphs
from chunker import chunk_paragraphs

RAW_DIR = os.path.join("data", "raw")

for name in ["10822802.json", "9870175.json"]:
    with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
        rec = json.load(f)
    chunks = chunk_paragraphs(extract_paragraphs(rec["text"]))
    print(f"=== {name} | {len(chunks)} chunks")
    for i in range(len(chunks) - 1):
        if chunks[i].rstrip().endswith(";"):
            print("  ends:  ", chunks[i][-100:])
            print("  next:  ", chunks[i + 1][:100])
            print()