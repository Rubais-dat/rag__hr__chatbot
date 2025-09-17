import os
import pandas as pd
import numpy as np
import faiss
from embedding import embed_text
from rag_pipeline import RAGPipeline
from groq import Groq
import ast # <-- Add this line

# Load API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment variables")

client = Groq(api_key=GROQ_API_KEY)
rag_pipeline = RAGPipeline()

# Load embeddings
EMBEDDINGS_FILE = "data/HR_policy_embeddings_local.csv"
df = pd.read_csv(EMBEDDINGS_FILE)

# Convert embeddings from string to numpy array using ast.literal_eval
vectors = np.stack(df['embedding'].apply(ast.literal_eval)) # <-- Corrected line

# Build FAISS index
dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vectors)
print(f"FAISS index built with {vectors.shape[0]} vectors.")

def ask_llm(question, context_chunks):
    # Combine context chunks into prompt
    context_text = "\n\n".join([c['text'] for c in context_chunks])
    prompt = f"Answer the question based on the following context:\n{context_text}\n\nQuestion: {question}\nAnswer:"

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_completion_tokens=1000
        )
        # Handle non-streaming response
        answer = completion.choices[0].message.content
        return answer
    except Exception as e:
        return f"Error: {e}"
    
def query(question, top_k=5):
    # Embed query and search FAISS
    context_chunks = rag_pipeline.run(question, top_k)
    return context_chunks

# Interactive query loop
if __name__ == "__main__":
    while True:
        q = input("Enter your query (or 'exit' to quit):\n> ")
        if q.lower() in ['exit', 'quit']:
            break

        context_chunks = query(q)
        answer = ask_llm(q, context_chunks)
        print("\nAnswer:\n", answer)
        print("\n" + "-"*50 + "\n")