import chromadb
import os
import google.generativeai as genai
from sailing_documents_with_metadata import exampleSourceDocuments

DATABASE_FILE_PATH = "./chroma_db_data"
COLLECTION_NAME = "sailing_knowledge_base_with_metadata"

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
    collection = client.get_or_create_collection(name=COLLECTION_NAME)

    if collection.count() == len(exampleSourceDocuments):
        print("Collection already initialized with example documents.")
        return

    # Unpack texts and metadata from the structured document list
    texts = [doc["text"] for doc in exampleSourceDocuments]
    metadatas = [doc["metadata"] for doc in exampleSourceDocuments]
    ids = [str(i) for i in range(len(exampleSourceDocuments))]

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )
    print(f"Inserted {len(exampleSourceDocuments)} documents into the collection.")
    print("Vector database initialized successfully.")


def queryVectorDb(query, source_type_filter=None):
    print(f"\nQuerying vector database for: '{query}'")

    client = chromadb.PersistentClient(path=DATABASE_FILE_PATH)
    collection = client.get_collection(name=COLLECTION_NAME)

    # Optional: filter results to a specific source_type using ChromaDB's where clause
    where_clause = {"source_type": source_type_filter} if source_type_filter else None

    results = collection.query(
        query_texts=[query],
        n_results=5,
        where=where_clause,
        include=["documents", "metadatas", "distances"]
    )
    print(f"Found {len(results['documents'][0])} matching documents.")
    return results


def create_context_with_sources(question, source_type_filter=None):
    """Build a context string that includes inline source references for each chunk."""
    results = queryVectorDb(question, source_type_filter)

    context_parts = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        source_ref = (
            f"[Source: {meta['source_title']}, "
            f"{meta['section']} — {meta['source_url']}]"
        )
        context_parts.append(f"{doc}\n{source_ref}")

    # Also return metadata separately so the caller can display a source list
    return "\n\n".join(context_parts), results["metadatas"][0]


def rag_query_with_citations(question, source_type_filter=None):
    context, retrieved_metadatas = create_context_with_sources(question, source_type_filter)

    prompt = f"""You are a sailing race official assistant for the 2026 Emerald Bay Championship.
Answer the question using ONLY the information provided in the context below.
For every fact you include in your answer, cite the source using the label provided
in the [Source: (source_title), (source_url)] tag that follows each passage.
If the context does not contain enough information to answer, say so clearly.

Context:
{context}

Question: {question}
Answer:"""

    response = model.generate_content(prompt)
    answer = response.text.strip()

    return answer, retrieved_metadatas


def query_without_rag(question):
    prompt = f"Question: {question}\nAnswer:"
    response = model.generate_content(prompt)
    return response.text.strip()


def print_sources(metadatas):
    print("\nSources consulted:")
    seen = set()
    for meta in metadatas:
        key = meta["source_url"]
        if key not in seen:
            seen.add(key)
            print(f"  [{meta['source_type']}] {meta['source_title']}")
            print(f"    Section : {meta['section']}")
            print(f"    URL     : {meta['source_url']}")
            print(f"    Issued  : {meta['published_date']} by {meta['published_by']}")


# ---------------------------------------------------------------------------
# Initialize the database
# ---------------------------------------------------------------------------

initVectorDb()

# ---------------------------------------------------------------------------
# Demo queries
# ---------------------------------------------------------------------------

DIVIDER = "=" * 70

# --- Query 1: Flag signal question ---
query1 = "What does a purple checkered flag mean?"

print(f"\n{DIVIDER}")
print("QUERY 1 (with RAG + citations)")
print(DIVIDER)
answer1, metas1 = rag_query_with_citations(query1)
print(f"Question : {query1}")
print(f"\nAnswer   :\n{answer1}")
print_sources(metas1)

print(f"\n{DIVIDER}")
print("QUERY 1 (without RAG — no context)")
print(DIVIDER)
print(f"Question : {query1}")
print(f"\nAnswer   :\n{query_without_rag(query1)}")

# --- Query 2: Hazard / safety question ---
# query2 = "Are there any depth hazards I should be aware of near the course?"

# print(f"\n{DIVIDER}")
# print("QUERY 2 (with RAG + citations)")
# print(DIVIDER)
# answer2, metas2 = rag_query_with_citations(query2)
# print(f"Question : {query2}")
# print(f"\nAnswer   :\n{answer2}")
# print_sources(metas2)

# # --- Query 3: Metadata-filtered query (Sailing Instructions only) ---
# query3 = "What are the rules for the Masters division?"

# print(f"\n{DIVIDER}")
# print("QUERY 3 (Sailing Instructions only — metadata filter demo)")
# print(DIVIDER)
# answer3, metas3 = rag_query_with_citations(query3, source_type_filter="sailing_instructions")
# print(f"Question : {query3}")
# print(f"Filter   : source_type = 'sailing_instructions'")
# print(f"\nAnswer   :\n{answer3}")
# print_sources(metas3)
