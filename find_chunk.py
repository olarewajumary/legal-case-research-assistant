import json

with open("data/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

needle = "so likely to result in the violation of constitutional rights"
for c in chunks:
    if needle in c["text"]:
        print(c["chunk_id"], "|", c["case_name"], "|", c["court_id"], c["date_filed"])
        print(c["url"])
        print()
        print(c["text"])