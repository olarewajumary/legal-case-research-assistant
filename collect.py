import json
import os
from cl_client import cl_get

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

TEXT_FIELDS = ["html_with_citations", "xml_harvard", "plain_text"]

resp = cl_get("search/", {"q": "qualified immunity", "type": "o", "court": "ca9"})
print("search status:", resp.status_code)
hits = resp.json()["results"][:10]

for hit in hits:
    opinion_id = hit["opinions"][0]["id"]
    path = os.path.join(RAW_DIR, f"{opinion_id}.json")

    if os.path.exists(path):
        print(opinion_id, "already saved, skipping")
        continue

    r = cl_get(f"opinions/{opinion_id}/")
    if r.status_code != 200:
        print(opinion_id, "status:", r.status_code, "- not saved")
        continue
    opinion = r.json()

    source = next((f for f in TEXT_FIELDS if opinion.get(f)), None)
    if source is None:
        print(opinion_id, "no text in any field - not saved")
        continue

    record = {
        "opinion_id": opinion_id,
        "cluster_id": hit["cluster_id"],
        "case_name": hit["caseName"],
        "court_id": hit["court_id"],
        "date_filed": hit["dateFiled"],
        "citation": hit["citation"],
        "url": "https://www.courtlistener.com" + hit["absolute_url"],
        "text_source": source,
        "text": opinion[source],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f)
    print(opinion_id, "saved from", source)

print("\nfiles in data/raw:")
for name in sorted(os.listdir(RAW_DIR)):
    size = os.path.getsize(os.path.join(RAW_DIR, name))
    print(" ", name, size, "bytes")