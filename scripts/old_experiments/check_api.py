import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("COURTLISTENER_TOKEN")

url = "https://www.courtlistener.com/api/rest/v4/search/"
params = {"q": "qualified immunity", "type": "o", "page_size": 3}
headers = {"Authorization": f"Token {token}"}

response = requests.get(url, params=params, headers=headers)
print("status:", response.status_code)

data = response.json()
print("top-level keys:", list(data.keys()))
print("total matches:", data.get("count"))
print("keys on one result:", list(data["results"][0].keys()))

first = data["results"][0]
print("case:", first["caseName"])
print("court:", first["court_id"], "| filed:", first["dateFiled"])
print("number of opinions:", len(first["opinions"]))
print("keys on one opinion:", list(first["opinions"][0].keys()))