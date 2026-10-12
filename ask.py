import re
from answer_v2 import get_claims, squash
from judge import judge
import llm


def verify_claims(sources, claims):
    kept = []
    for c in claims:
        n = c.get("source")
        if not (isinstance(n, int) and 1 <= n <= len(sources)):
            continue
        src = sources[n - 1]
        try:
            label, raw = judge(c.get("statement", ""), src["text"])
        except Exception as e:
            print("   judge failed:", type(e).__name__)
            continue
        match = re.search(r"QUOTE:\s*(.*?)\s*LABEL:", raw, re.DOTALL)
        quote = match.group(1).strip() if match else ""
        if label == "ASSERTS" and quote and squash(quote) in squash(src["text"]):
            kept.append({
                "statement": c["statement"],
                "quote": quote,
                "case_name": src["case_name"],
                "court": src["court_id"],
                "date_filed": src["date_filed"],
                "url": src["url"],
                "unpublished": src.get("unpublished", False),
            })
    return kept


def ask(question):
    models = {"writer": llm.describe("writer"), "judge": llm.describe("judge")}
    sources, claims = get_claims(question)
    if sources is None:
        return {"status": "refused", "message": "No relevant precedent found.", "claims": []}
    kept = verify_claims(sources, claims)
    if not kept:
        return {"status": "unverified",
                "message": "Passages were found, but no statement could be verified against them.",
                "claims": [], "models": models}
    return {"status": "answered", "message": None, "claims": kept, "models": models}


if __name__ == "__main__":
    for q in [
        "What does clearly established law mean for qualified immunity?",
        "What is the recipe for chocolate chip cookies?",
    ]:
        out = ask(q)
        print(f"\n=== {q}\nSTATUS: {out['status']}")
        if out["message"]:
            print(out["message"])
        if "models" in out:
            print(f"  writer: {out['models']['writer']} | judge: {out['models']['judge']}")    
        for c in out["claims"]:
            print(f"\n- {c['statement']}")
            print(f"  {c['case_name']} ({c['court']}, {c['date_filed']})")
            if c["unpublished"]:
                print("  WARNING: this opinion is marked by the court as unpublished and not precedent.")
            print(f"  \"{c['quote']}\"")
            print(f"  {c['url']}")