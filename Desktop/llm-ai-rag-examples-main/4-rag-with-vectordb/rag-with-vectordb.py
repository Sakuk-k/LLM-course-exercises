import chromadb
import os
import google.generativeai as genai
from sympy import pprint
from sailing_documents import exampleSourceDocuments

DATABASE_FILE_PATH = "./chroma_db_data"  # Path where ChromaDB will store its data

# Initialize environment variable for Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please set it.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash-lite')


def initVectorDb():
    print("Initializing vector database...")

    client = chromadb.PersistentClient(path=DATABASE_FILE_PATH)

    # get_or_create_collection avoids errors if the collection already exists
    # ChromaDB uses its built-in embedding model (all-MiniLM-L6-v2 via onnxruntime) by default
    collection = client.get_or_create_collection(name="sailing_knowledge_base")

    # Assume the collection is already initialized if it contains the same number of documents as our example set
    if collection.count() == len(exampleSourceDocuments):
        print("Collection already initialized with example documents.")
        return

    # Add documents - ChromaDB automatically generates embeddings for them
    collection.add(
        documents=exampleSourceDocuments,
        ids=[str(i) for i in range(len(exampleSourceDocuments))]
    )
    print(f"Inserted {len(exampleSourceDocuments)} documents into the collection.")
    print("Vector database initialized successfully.")

# Main RAG function
def rag_query(question):
    # Retrieve context
    context = create_context_from_vector_db(question)
    # Create prompt for Gemini
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    # Get response from Gemini
    answer = query_gemini(prompt)
    return answer

# Query Gemini API
def query_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

# Retrieve context from vector database
def create_context_from_vector_db(question):
    results = queryVectorDb(question)
    # Extract text from search results to create context
    return " ".join(results['documents'][0])


def queryVectorDb(query):
    print(f"Querying vector database for: {query}")

    client = chromadb.PersistentClient(path=DATABASE_FILE_PATH)
    collection = client.get_collection(name="sailing_knowledge_base")

    # ChromaDB automatically embeds the query text using the same built-in model
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    print(f"Found {len(results['documents'][0])} results for the query.")
    #print("Results:")
    #pprint(results)
    return results

def query_without_rag(question):
    prompt = f"Question: {question}\nAnswer:"
    # Get response from Gemini
    answer = query_gemini(prompt)
    return answer


initVectorDb()  # Initialize the vector database and insert example documents

##
## Now we can perform a similarity search on the collection.
##

# Here is our example search query in plain text.
# search_query = "Where is the Regatta Office? Emerald Bay Championship 2026"
search_query = "What does a purple checkered flag mean?"
# search_query = "Who won last year?"
# search_query = "What is the penalty for tacking in Obsidian Reach?"

RAGresults = rag_query(search_query)
print("RAG Results\n###########################################################")
# Print the results
print(f"Query: {search_query}")
print(f"LLM Response: {RAGresults}\n")

print("************************************************************")
NoContextResults = query_without_rag(search_query)
print("No RAG Results\n###########################################################")
print(f"Query: {search_query}")
print(f"LLM Response: {NoContextResults}\n")
