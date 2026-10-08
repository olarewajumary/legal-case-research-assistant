import json
import numpy as np
from sentence_transformers import SentenceTransformer

with open("data/chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")
texts = [c["text"] for c in chunks]
embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

np.save("data/embeddings.npy", embeddings)
print("embeddings shape:", embeddings.shape)