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


PROVIDERS = {"groq": _groq_chat}


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