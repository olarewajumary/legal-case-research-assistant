import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("COURTLISTENER_TOKEN")
headers = {"Authorization": f"Token {token}"}

base = "https://www.courtlistener.com/api/rest/v4"
courts = ["scotus", "ca9", "ca5"]
fields = ["plain_text", "html", "html_lawbox", "html_columbia",
          "html_anon_2020", "xml_harvard", "html_with_citations"]

for court in courts:
    params = {"q": "qualified immunity", "type": "o", "court": court}
    resp = requests.get(f"{base}/search/", params=params, headers=headers)
    print(court, "search status:", resp.status_code)
    if resp.status_code != 200:
        print(resp.text[:300])
        break

    hits = resp.json()["results"][:4]
    time.sleep(2)

    for hit in hits:
        opinion_id = hit["opinions"][0]["id"]
        r = requests.get(f"{base}/opinions/{opinion_id}/", headers=headers)
        if r.status_code != 200:
            print(opinion_id, "status:", r.status_code, r.text[:200])
            break
        opinion = r.json()
        filled = {n: len(opinion.get(n) or "") for n in fields if opinion.get(n)}
        print(court, opinion_id, filled or "ALL EMPTY")
        time.sleep(2)