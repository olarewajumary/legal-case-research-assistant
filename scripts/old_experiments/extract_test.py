from collections import Counter
from bs4 import BeautifulSoup
from cl_client import cl_get

resp = cl_get("opinions/4289306/")
print("status:", resp.status_code)
html = resp.json()["html_with_citations"]

print("total chars:", len(html))
print("first 500 chars:")
print(html[:500])

soup = BeautifulSoup(html, "html.parser")
tags = Counter(tag.name for tag in soup.find_all(True))
print("tags found:", dict(tags))