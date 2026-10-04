import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("COURTLISTENER_TOKEN")
headers = {"Authorization": f"Token {token}"}

search_url = "https://www.courtlistener.com/api/rest/v4/search/"
params = {"q": "qualified immunity", "type": "o", "court": "scotus", "page_size": 1}
hit = requests.get(search_url, params=params, headers=headers).json()["results"][0]

opinion_id = hit["opinions"][0]["id"]
print("case:", hit["caseName"], "| court:", hit["court_id"])
print("opinion id:", opinion_id)

opinion_url = f"https://www.courtlistener.com/api/rest/v4/opinions/{opinion_id}/"
resp = requests.get(opinion_url, headers=headers)
print("status:", resp.status_code)

opinion = resp.json()
print("keys:", list(opinion.keys()))

text_fields = ["plain_text", "html", "html_lawbox", "html_columbia",
               "html_anon_2020", "xml_harvard", "html_with_citations"]

for name in text_fields:
    value = opinion.get(name) or ""
    print(f"{name}: {len(value)} characters")

print("\n--- xml_harvard (first 600 chars) ---")
print(opinion["xml_harvard"][:600])

print("\n--- html_with_citations (first 600 chars) ---")
print(opinion["html_with_citations"][:600])
print("\n--- xml_harvard only ---")
print(opinion["xml_harvard"][:600])