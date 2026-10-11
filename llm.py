import os
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "groq")


def _groq_chat(messages, role):
    from groq import Groq

    models = {"writer": os.getenv("GROQ_MODEL"), "judge": os.getenv("GROQ_JUDGE_MODEL")}
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model=models[role], messages=messages, temperature=0
    )
    choice = response.choices[0]
    return choice.message.content or "", choice.finish_reason, models[role]


def _ollama_chat(messages, role):
    import requests

    model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": 0},
        },
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()
    text = data["message"]["content"] or ""
    return text, data.get("done_reason"), model

PROVIDERS = {"groq": _groq_chat, "ollama": _ollama_chat}

def chat(messages, role="writer"):
    """Send messages to the configured provider. Returns (text, finish_reason, model_name)."""
    if PROVIDER not in PROVIDERS:
        raise ValueError(f"Unknown LLM_PROVIDER: {PROVIDER}. Known: {list(PROVIDERS)}")
    return PROVIDERS[PROVIDER](messages, role)


if __name__ == "__main__":
    messages = [{"role": "user", "content": "Reply with the single word: ready"}]
    for role in ["writer", "judge"]:
        text, finish, model = chat(messages, role)
        print(f"provider: {PROVIDER} | role: {role} | model: {model} | finish: {finish} | reply: {text.strip()[:40]}")