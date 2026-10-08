import os
from cl_client import cl_get

RAW_DIR = os.path.join("data", "raw")
saved = {int(name.split(".")[0]) for name in os.listdir(RAW_DIR)}

resp = cl_get("search/", {"q": "qualified immunity", "type": "o", "court": "ca9"})
print("status:", resp.status_code)

for hit in resp.json()["results"][:10]:
    for op in hit["opinions"]:
        mark = "SAVED" if op["id"] in saved else "     "
        print(mark, op["id"], op["type"], "|", hit["caseName"][:35])     