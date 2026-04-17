# RAG with ChromaDB and Gemini

This script demonstrates a Retrieval Augmented Generation (RAG) pipeline. It uses ChromaDB as a local vector database to store sailing knowledge documents, retrieves the most relevant context for a query, and passes that context to the Gemini LLM to produce a grounded answer. A second query is run without context to illustrate the difference RAG makes.

---

## Key Concepts Covered

* **Retrieval Augmented Generation (RAG)** — enriching an LLM prompt with relevant context retrieved from a vector database to produce more accurate, grounded answers.
* **ChromaDB PersistentClient** — stores the vector database on disk so it survives between runs. Uses the same `./chroma_db_data` path as example 3.
* **Built-in embeddings** — ChromaDB automatically converts documents and queries into vector embeddings using the default `all-MiniLM-L6-v2`. No external embedding model required.
* **RAG vs. no-RAG comparison** — the script runs the same question both with and without retrieved context so you can compare the quality of responses.

---

## Prerequisites

* **Python 3.8+**
* **Gemini API key** — set the `GEMINI_API_KEY` environment variable before running. Get your gey from https://aistudio.google.com/ or https://console.cloud.google.com/ if you don't have one.

### Installing Python Dependencies

Activate the virtual environment before installing dependencies or running any demo.

* **Windows (Command Prompt):**
    ```
    venv\Scripts\activate
    ```
* **Windows (PowerShell):**
    ```
    .\venv\Scripts\Activate.ps1
    ```
* **Linux/macOS:**
    ```
    source venv/bin/activate
    ```

Once activated, you'll see `(venv)` at the start of your terminal prompt.

Then, install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

---

## Getting Started

### 1. Set Your API Key

```bash
# On Windows:
set GEMINI_API_KEY=your_api_key_here

# On macOS/Linux:
export GEMINI_API_KEY=your_api_key_here
```

### 2. Run the Code

```bash
python rag-with-vectordb.py
```

The script will:
* **Initialize the vector database** — connect to ChromaDB, create the `sailing_knowledge_base` collection if it doesn't exist, and insert the example sailing documents.
* **Run a RAG query** — retrieve the most relevant documents for the search query and pass them as context to Gemini.
* **Run a no-context query** — send the same question to Gemini without any retrieved context.
* **Print both answers** so you can compare the results.

---

## Code Overview

### `initVectorDb()` Function

Sets up the ChromaDB collection and inserts the example documents from `sailing_documents.py`:

* **`chromadb.PersistentClient(path=DATABASE_FILE_PATH)`** — opens or creates the on-disk database.
* **`client.get_or_create_collection(name="sailing_knowledge_base")`** — creates the collection if it doesn't exist, or opens it if it does.
* **`collection.count()`** — checked before inserting to skip re-initialization if the collection is already populated.
* **`collection.add(documents=..., ids=...)`** — inserts documents; ChromaDB automatically generates embeddings.

### `queryVectorDb(query)` Function

Performs a semantic similarity search and returns the closest matching documents:

* **`collection.query(query_texts=..., n_results=5)`** — ChromaDB automatically embeds the query and returns the top 5 matching documents with distance scores.

### `create_context(question)` Function

Calls `queryVectorDb()` and joins the returned documents into a single context string to be injected into the LLM prompt.

### `rag_query(question)` Function

Builds a prompt from the retrieved context and the question, then calls Gemini to generate a grounded answer.

### `query_with_rag(question)` Function

Sends the question directly to Gemini without any retrieved context, for comparison.

---

## Extending the Knowledge Base

To add more documents to your `sailing_knowledge_base`:

1. Add new strings to the `exampleSourceDocuments` list in `sailing_documents.py`.
2. Delete the existing collection so it gets rebuilt on the next run: `client.delete_collection("sailing_knowledge_base")`.

---
