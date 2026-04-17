import os
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Initialize environment variable for Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set it.")

# Configure Gemini API
print("Configuring Gemini API...")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')
print("Gemini API configured.")

# Initialize sentence transformer for embeddings
print("Loading sentence transformer model...")
embedder = SentenceTransformer('all-MiniLM-L6-v2')
print("Sentence transformer model loaded.")

# Sample knowledge base (in-memory list; could be loaded from a file)
knowledge_base = [
    "The 1991 edition of the MAOL tables is blue-red in color",
    "Maxines's 7-year-old favorite food is Hesburger.",
    "Finnish Hornet crashed as part of an aerobatic display in May 2025."
]
print(f"Knowledge base loaded with {len(knowledge_base)} entries.")

# Compute embeddings for the knowledge base
print("Computing knowledge base embeddings...")
knowledge_embeddings = embedder.encode(knowledge_base)
print("Embeddings computed.")

# Compute cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Retrieve relevant context
def retrieve_context(query, top_k=2):
    print(f"Retrieving top {top_k} context entries for query...")
    query_embedding = embedder.encode([query])[0]
    similarities = [cosine_similarity(query_embedding, emb) for emb in knowledge_embeddings] 

    embeddingSimilarities = list(zip(similarities, knowledge_base))

    print("Similarity scores:")
    for a in embeddingSimilarities:
        print(f"{a[0]}, {a[1]}") 

    top_indices = np.argsort(similarities)[::-1][:top_k]
    context = [knowledge_base[i] for i in top_indices]
    
    print(f"Retrieved context:\n  " + "\n  ".join(context))
    return "\n".join(context)

# Query Gemini API
def query_gemini(prompt):
    print("Sending prompt to Gemini API...")
    response = model.generate_content(prompt)
    print("Response received from Gemini API.")
    return response.text.strip()

# Main RAG function
def rag_query(question):
    print(f"\nQuestion: {question}")
    # Retrieve context
    context = retrieve_context(question)
    # Create prompt for Gemini
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    # Get response from Gemini
    answer = query_gemini(prompt)
    return answer

# Example query
question = "Tell me the colors of the MAOL tables of different years"
answer = rag_query(question)
print(f"\nAnswer: {answer}")