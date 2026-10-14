import json
import os
from text_extract import extract_paragraphs
from chunker import chunk_paragraphs
from clean_text import remove_page_markers

RAW_DIR = os.path.join("data", "raw")
OUT_PATH = os.path.join("data", "chunks.json")
MARKERS = ["not appropriate for publication", "not precedent"]

all_chunks = []
flagged = []
for name in sorted(os.listdir(RAW_DIR)):
    with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
        rec = json.load(f)
    paragraphs = extract_paragraphs(rec["text"])
    paragraphs = [remove_page_markers(p) for p in paragraphs]
    full_text = " ".join(" ".join(paragraphs).lower().split())
    unpublished = any(m in full_text for m in MARKERS)
    if unpublished:
        flagged.append((rec["opinion_id"], rec["case_name"]))

    for i, text in enumerate(chunk_paragraphs(paragraphs)):
        all_chunks.append({
            "chunk_id": f"{rec['opinion_id']}-{i}",
            "opinion_id": rec["opinion_id"],
            "chunk_index": i,
            "case_name": rec["case_name"],
            "court_id": rec["court_id"],
            "date_filed": rec["date_filed"],
            "citation": rec["citation"],
            "url": rec["url"],
            "unpublished": unpublished,
            "text": text,
        })

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f)

print("chunks written:", len(all_chunks))
print("unique chunk ids:", len({c["chunk_id"] for c in all_chunks}))
print("flagged unpublished opinions:", len(flagged))
for oid, case in flagged:
    print("  ", oid, case)