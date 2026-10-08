import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

models = client.models.list().data
print("models available to this key:", len(models))
for m in sorted(models, key=lambda m: m.id):
    print(" ", m.id, "| context:", getattr(m, "context_window", "?"), "| owner:", m.owned_by)