import re
from bs4 import BeautifulSoup
from cl_client import cl_get


def extract_paragraphs(html):
    """Turn either layout (<p> tags or <pre> blocks) into a clean list of paragraphs."""
    soup = BeautifulSoup(html, "html.parser")

    p_tags = soup.find_all("p")
    if p_tags:
        raw = [p.get_text(" ", strip=True) for p in p_tags]
    else:
        text = soup.get_text()
        raw = re.split(r"\n\s*\n", text)

    cleaned = [re.sub(r"\s+", " ", chunk).strip() for chunk in raw]
    return [c for c in cleaned if c]


if __name__ == "__main__":
    for opinion_id in [8401475, 4289306]:
        resp = cl_get(f"opinions/{opinion_id}/")
        print(f"\nopinion {opinion_id} status:", resp.status_code)
        paras = extract_paragraphs(resp.json()["html_with_citations"])
        print("paragraph count:", len(paras))
        print("longest paragraph (chars):", max(len(p) for p in paras))
        for p in paras[:3]:
            print("  -", p[:120])