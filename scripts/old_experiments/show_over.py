import json
import os
from sentence_transformers import SentenceTransformer
from text_extract import extract_paragraphs
from chunker import chunk_paragraphs

model = SentenceTransformer("all-MiniLM-L6-v2")
RAW_DIR = os.path.join("data", "raw")

for name in sorted(os.listdir(RAW_DIR)):
    with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
        rec = json.load(f)
    for chunk in chunk_paragraphs(extract_paragraphs(rec["text"])):
        tokens = len(model.tokenizer(chunk)["input_ids"])
        if tokens > model.max_seq_length:
            print(f"--- {name} | {len(chunk)} chars | {tokens} tokens")
            print(chunk[:300])
            print("  ...")
            print(chunk[-200:])
            print()