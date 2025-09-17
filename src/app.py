import os
import pandas as pd
import numpy as np
import faiss
import ast
from flask import Flask, request, jsonify
from embedding import embed_text  
from rag_pipeline import RAGPipeline
from groq import Groq

# Initialize Flask App
app = Flask(__name__)

# Load API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in environment variables")

client = Groq(api_key=GROQ_API_KEY)

# Initialize RAG Pipeline components
rag_pipeline = RAGPipeline()
EMBEDDINGS_FILE = "data/HR_policy_embeddings_local.csv"

# Load embeddings and build FAISS index
df = pd.read_csv(EMBEDDINGS_FILE)
vectors = np.stack(df['embedding'].apply(ast.literal_eval))
dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vectors)
print(f"FAISS index built with {vectors.shape[0]} vectors.")

def ask_llm(question, context_chunks):
    context_text = "\n\n".join([c['text'] for c in context_chunks])
    prompt = f"Answer the question based on the following context:\n{context_text}\n\nQuestion: {question}\nAnswer:"
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_completion_tokens=1000
        )
        answer = completion.choices[0].message.content
        return answer
    except Exception as e:
        return f"Error: {e}"

# Define the API endpoint
@app.route('/query', methods=['POST'])
def query_api():
    
    data = request.get_json()
    question = data.get('question')
    
    if not question:
        return jsonify({"error": "No 'question' field provided in the request."}), 400
    
    # 1. Retrieve relevant chunks (Retrieval)
    context_chunks = rag_pipeline.run(question)
    
    # 2. Get the answer from the LLM (Generation)
    answer = ask_llm(question, context_chunks)
    
    # 3. Prepare the sources for the response
    sources = [
        {"text": chunk['text'], "score": chunk['score']}
        for chunk in context_chunks
    ]
    
    
    return jsonify({
        "answer": answer,
        "sources": sources
    })

# Run the API server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)