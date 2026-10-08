import json
import os
from text_extract import extract_paragraphs

RAW_DIR = os.path.join("data", "raw")

for name in sorted(os.listdir(RAW_DIR)):
    with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
        rec = json.load(f)
    paras = extract_paragraphs(rec["text"])
    chars = sum(len(p) for p in paras)
    print(f"{rec['opinion_id']} | {rec['date_filed']} | {len(paras):3} paras | {chars:6} chars | {rec['case_name'][:50]}")