# ChromaDB Sailing Knowledge Base

This script demonstrates the core concepts of a vector database using ChromaDB. It builds a small sailing knowledge base by storing text documents as vector embeddings, then performs semantic similarity searches against them.

---

## Key Concepts Covered

* **Creating and persisting a ChromaDB collection** using `PersistentClient`, which stores data on disk so it survives between runs.
* **Built-in embeddings** — ChromaDB automatically converts text into vector embeddings using `all-MiniLM-L6-v2` via `onnxruntime`. No external embedding model or manual encoding is required.
* **Semantic similarity search** using natural language, and interpreting the distance scores returned (lower score = more similar).

---

## Prerequisites

Before running this script, make sure you have the following:

* **Python 3.8+**

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

### 1. Run the Code

Execute the script from your terminal:

```bash
python vectordb-intro.py
```


## Code Overview

### `initVectorDb()` Function

Sets up the ChromaDB collection and inserts the example documents.


### `queryVectorDb(query)` Function

Performs a semantic similarity search against the collection. It takes a natural language query, which is automatically converted to an embedding using the built-in model and returns the closest matching documents along with their distance scores.

### Main Execution Block

Calls `initVectorDb()` to ensure the collection is populated, then calls `queryVectorDb()` with a sample query and prints each result with its distance score.

---

## Extending the Knowledge Base

To add more documents to your `sailing_knowledge_base`:

1.  Add new strings to the `exampleSourceDocuments` list in `initVectorDb()`.
2.  The script checks `collection.count()` to detect an already-initialized collection. If you add documents, delete the existing collection first so it gets rebuilt: `client.delete_collection("sailing_knowledge_base")`.

---
