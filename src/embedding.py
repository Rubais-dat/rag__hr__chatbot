import os
import csv
import torch
from transformers import AutoTokenizer, AutoModel

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
CLEANED_FILE = "data/HR_policy_cleaned.txt"
EMBEDDINGS_FILE = "data/HR_policy_embeddings_local.csv"

model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.squeeze().tolist()

# Read cleaned text
with open(CLEANED_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Split into chunks
chunks = []
start = 0
while start < len(text):
    end = start + CHUNK_SIZE
    chunks.append(text[start:end])
    start += CHUNK_SIZE - CHUNK_OVERLAP

# Generate embeddings
embeddings = [embed_text(chunk) for chunk in chunks]

# Save embeddings
os.makedirs(os.path.dirname(EMBEDDINGS_FILE), exist_ok=True)
with open(EMBEDDINGS_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["chunk_id", "chunk_text", "embedding"])
    for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
        writer.writerow([i, chunk, vector])

print(f"Total chunks: {len(chunks)}")
print(f"Embeddings saved to {EMBEDDINGS_FILE}")
