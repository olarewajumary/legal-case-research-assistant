import json
import os
from text_extract import extract_paragraphs

RAW_DIR = os.path.join("data", "raw")
rows = []

for name in sorted(os.listdir(RAW_DIR)):
    with open(os.path.join(RAW_DIR, name), encoding="utf-8") as f:
        rec = json.load(f)
    paras = extract_paragraphs(rec["text"])
    rows.append((sum(len(p) for p in paras), len(paras), rec["opinion_id"], rec["case_name"]))

sizes = sorted(r[0] for r in rows)
print("opinions:", len(rows))
print("chars  min / median / max:", sizes[0], "/", sizes[len(sizes) // 2], "/", sizes[-1])

print("\nunder 3000 chars:")
for chars, n, oid, case in sorted(rows):
    if chars < 3000:
        print(f"  {oid} | {n} paras | {chars} chars | {case[:50]}")