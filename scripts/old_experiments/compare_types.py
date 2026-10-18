import re
from cl_client import cl_get
from text_extract import extract_paragraphs


def squash(text):
    """Lowercase and keep only letters and digits, so punctuation/spacing can't break a match."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


texts = {}
for label, oid in [("lead", 9870175), ("combined", 4106049)]:
    r = cl_get(f"opinions/{oid}/")
    print(label, oid, "status:", r.status_code)
    o = r.json()
    html = o.get("html_with_citations") or ""
    paras = extract_paragraphs(html) if html else []
    texts[label] = " ".join(paras)
    print("  raw chars:", len(html), "| paragraphs:", len(paras), "| clean chars:", len(texts[label]))

lead = squash(texts["lead"])
combined = squash(texts["combined"])

hits = 0
points = list(range(5, 100, 10))
for pct in points:
    start = len(lead) * pct // 100
    probe = lead[start:start + 50]
    found = probe in combined
    hits += found
    print(f"  probe at {pct:2}%: {'found' if found else 'MISSING'}")

print(f"\nfound {hits} of {len(points)} probes")