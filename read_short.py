import json
import os

RAW_DIR = os.path.join("data", "raw")

for oid in [8623046, 8451242, 8625377]:
    with open(os.path.join(RAW_DIR, f"{oid}.json"), encoding="utf-8") as f:
        rec = json.load(f)
    print(f"--- {oid} | {rec['case_name']} | source: {rec['text_source']}")
    print(rec["text"][:700])
    print()