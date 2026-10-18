from cl_client import cl_get

resp = cl_get("search/", {"q": "qualified immunity", "type": "o", "court": "ca9"})
print("status:", resp.status_code)

for hit in resp.json()["results"][:10]:
    types = [o["type"] for o in hit["opinions"]]
    print(hit["cluster_id"], "|", hit["status"], "|", len(types), "opinion(s):", types, "|", hit["caseName"][:35])