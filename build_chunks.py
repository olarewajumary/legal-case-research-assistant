import json
import os
from text_extract import extract_paragraphs
from chunker import chunk_paragraphs

RAW_DIR = os.path.join("data", "raw")
OUT_PATH = os.path.join("data", "chunks.json")

all_chunks = []
for name in sorted(os.listdir(RAW_DIR)):
    with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
        rec = json.load(f)
    chunks = chunk_paragraphs(extract_paragraphs(rec["text"]))
    for i, text in enumerate(chunks):
        all_chunks.append({
            "chunk_id": f"{rec['opinion_id']}-{i}",
            "opinion_id": rec["opinion_id"],
            "chunk_index": i,
            "case_name": rec["case_name"],
            "court_id": rec["court_id"],
            "date_filed": rec["date_filed"],
            "citation": rec["citation"],
            "url": rec["url"],
            "text": text,
        })

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f)

print("chunks written:", len(all_chunks))
print("unique chunk ids:", len({c["chunk_id"] for c in all_chunks}))
print("file size (bytes):", os.path.getsize(OUT_PATH))
print("example:", all_chunks[0]["chunk_id"], "|", all_chunks[0]["case_name"][:40])