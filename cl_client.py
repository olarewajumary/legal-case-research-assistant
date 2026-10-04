import os
import re
import time
import requests
from dotenv import load_dotenv

load_dotenv()
HEADERS = {"Authorization": f"Token {os.getenv('COURTLISTENER_TOKEN')}"}
BASE = "https://www.courtlistener.com/api/rest/v4"


def cl_get(path, params=None, max_tries=5):
    """GET from CourtListener. If throttled (429), wait and retry."""
    for attempt in range(1, max_tries + 1):
        resp = requests.get(f"{BASE}/{path}", params=params, headers=HEADERS)
        if resp.status_code != 429:
            return resp

        match = re.search(r"available in (\d+) seconds", resp.text)
        wait = int(match.group(1)) + 2 if match else 20
        print(f"throttled (try {attempt}/{max_tries}), waiting {wait}s...")
        time.sleep(wait)

    raise RuntimeError("Still throttled after retries")


if __name__ == "__main__":
    r = cl_get("search/", {"q": "qualified immunity", "type": "o", "court": "ca9"})
    print("status:", r.status_code)
    for hit in r.json()["results"][:4]:
        oid = hit["opinions"][0]["id"]
        o = cl_get(f"opinions/{oid}/")
        filled = {n: len(o.json().get(n) or "")
                  for n in ["plain_text", "html_lawbox", "html_columbia",
                            "html_anon_2020", "xml_harvard", "html_with_citations"]
                  if o.json().get(n)}
        print(hit["court_id"], oid, filled or "ALL EMPTY")