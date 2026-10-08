import os
from dotenv import load_dotenv
from groq import Groq
from gate import retrieve, chunks

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL")

SYSTEM = (
    "You are a legal research assistant. Answer the question using ONLY the numbered "
    "sources provided. Cite each claim with its source number in square brackets, like [1]. "
    "If the sources do not answer the question, say that they do not. "
    "Do not use outside knowledge and do not invent cases or citations."
)


def answer(question):
    result = retrieve(question)
    if not result["answerable"]:
        return {"answer": result["message"], "sources": [], "tokens": 0}

    sources = [chunks[i] for i, _ in result["chunks"]]
    context = "\n\n".join(
        f"[{n}] {c['case_name']} ({c['court_id']}, filed {c['date_filed']})\n{c['text']}"
        for n, c in enumerate(sources, 1)
    )
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Sources:\n\n{context}\n\nQuestion: {question}"},
        ],
        temperature=0,
    )
    choice = response.choices[0]
    if choice.finish_reason != "stop":
        print("WARNING: finish reason was", choice.finish_reason)
    return {"answer": choice.message.content, "sources": sources, "tokens": response.usage.total_tokens}


if __name__ == "__main__":
    for q in [
        "What does clearly established law mean for qualified immunity?",
        "What is the recipe for chocolate chip cookies?",
    ]:
        out = answer(q)
        print(f"\nQUESTION: {q}")
        print("ANSWER:", out["answer"])
        print("TOKENS:", out["tokens"])
        for n, c in enumerate(out["sources"], 1):
            print(f"  [{n}] {c['chunk_id']} | {c['case_name'][:40]}")