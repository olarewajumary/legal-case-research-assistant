import json
import os

RAW_DIR = os.path.join("data", "raw")
PHRASES = ["not appropriate for publication", "not precedent"]

for name in sorted(os.listdir(RAW_DIR)):
    with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
        rec = json.load(f)
    text = " ".join(rec["text"].lower().split())
    found = [p for p in PHRASES if p in text]
    print(f"{rec['opinion_id']} | {len(rec['text']):6} chars | {found or 'no marker'} | {rec['case_name'][:40]}")