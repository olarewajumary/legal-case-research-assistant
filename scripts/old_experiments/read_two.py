import json
import os
from text_extract import extract_paragraphs

RAW_DIR = os.path.join("data", "raw")

for oid in [8623046, 8451242]:
    with open(os.path.join(RAW_DIR, f"{oid}.json"), encoding="utf-8") as f:
        rec = json.load(f)
    print(f"--- {oid} | {rec['case_name']} | {rec['date_filed']} | source: {rec['text_source']}")
    for p in extract_paragraphs(rec["text"]):
        print("  *", p)
    print()