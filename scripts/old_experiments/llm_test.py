import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL")
print("using model:", MODEL)

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You answer in one short sentence."},
            {"role": "user", "content": "What does 'precedent' mean in law?"},
        ],
        temperature=0,
    )
    choice = response.choices[0]
    print("answer:", choice.message.content)
    print("finish reason:", choice.finish_reason)
    print("tokens used:", response.usage.total_tokens)
except Exception as e:
    print("FAILED:", type(e).__name__, "-", e)