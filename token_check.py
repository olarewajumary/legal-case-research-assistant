import json
import os
from sentence_transformers import SentenceTransformer
from text_extract import extract_paragraphs
from chunker import chunk_paragraphs

model = SentenceTransformer("all-MiniLM-L6-v2")
limit = model.max_seq_length
print("model token limit:", limit)

RAW_DIR = os.path.join("data", "raw")
counts = []
for name in sorted(os.listdir(RAW_DIR)):
    with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
        rec = json.load(f)
    for chunk in chunk_paragraphs(extract_paragraphs(rec["text"])):
        counts.append(len(model.tokenizer(chunk)["input_ids"]))

counts.sort()
print("chunks:", len(counts))
print("tokens  median / max:", counts[len(counts) // 2], "/", counts[-1])
print("chunks over the limit:", sum(1 for c in counts if c > limit))