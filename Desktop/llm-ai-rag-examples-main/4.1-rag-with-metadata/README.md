# RAG with Metadata & Source Citations

This demo extends [4-rag-with-vectordb](../4-rag-with-vectordb/) to show how **document metadata** can be stored alongside embeddings in ChromaDB and used to produce **traceable, cited answers** from a RAG pipeline.

The knowledge base uses fictional sailing race documents drawn from realistic source types — Sailing Instructions, Notices to Competitors, event timetables, race results, and protest decisions — mimicking the kind of material published on platforms like manage2sail or event homepages.

---

## Key Concepts Covered

* **ChromaDB metadata** — storing structured fields (source type, URL, section, author) alongside each document chunk using the `metadatas` parameter in `collection.add()`.
* **Metadata retrieval** — requesting `include=["documents", "metadatas", "distances"]` in `collection.query()` so source information is returned with every result.
* **Source-aware context building** — embedding inline `[Source: ...]` tags in the retrieved context so the LLM can reference them directly in its answer.
* **Citation-instructed prompting** — prompting the LLM to cite every fact it uses, producing auditable, grounded answers.
* **Metadata filtering** — using ChromaDB's `where` clause to restrict a query to a specific `source_type` (e.g., only Sailing Instructions), demonstrated in Query 3.

---

## What Changed from Demo 4

| | Demo 4 | Demo 4.1 |
|---|---|---|
| Documents stored | Plain text strings | Text + structured metadata dict |
| `collection.add()` | `documents`, `ids` | `documents`, `metadatas`, `ids` |
| `collection.query()` | Returns documents only | Returns documents + metadatas + distances |
| Context building | Raw text joined | Text with `[Source: ...]` tags per chunk |
| LLM prompt | "Answer the question" | "Answer and cite your sources" |
| Output | Raw LLM answer | Cited answer + formatted source list |
| Filtering | None | `where={"source_type": "..."}` |

---

## Document Source Types

| `source_type` | Description | URL pattern |
|---|---|---|
| `sailing_instructions` | Official SI published by the Race Committee | `manage2sail.com/.../si#...` |
| `notice_to_competitors` | NTC notices with rule amendments and safety alerts | `manage2sail.com/.../ntc/ntc-00N` |
| `event_timetable` | Schedule and venue information | `emerald-bay-championship.example.com/...` |
| `race_results` | Historical finishing positions | `manage2sail.com/.../results/...` |
| `protest_decision` | Protest Committee rulings | `manage2sail.com/.../protests/...` |

---

## Prerequisites

* **Python 3.8+**
* **Gemini API key** — set the `GEMINI_API_KEY` environment variable. Get one at [Google AI Studio](https://aistudio.google.com/).

### Set Up the Virtual Environment

```bash
# Create and activate a virtual environment
python -m venv venv

# Windows (Command Prompt):
venv\Scripts\activate

# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# macOS/Linux:
source venv/bin/activate
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Demo

```bash
# Set your API key (Windows):
set GEMINI_API_KEY=your_api_key_here

# macOS/Linux:
export GEMINI_API_KEY=your_api_key_here

python rag-with-metadata.py
```

The script runs three demonstration queries:

1. **Flag signal question** — answered with RAG (with citations) vs. without RAG, to show the difference.
2. **Safety/hazard question** — shows how NTC documents surface with correct source references.
3. **Metadata-filtered query** — queries restricted to `source_type = "sailing_instructions"` using ChromaDB's `where` clause.

---

## Code Overview

### `sailing_documents_with_metadata.py`

Each document is a dict with two keys:
- `"text"` — the passage to embed and retrieve.
- `"metadata"` — a flat dict with `source_type`, `source_title`, `source_url`, `section`, `published_by`, and `published_date`.

### `initVectorDb()`

Unpacks texts and metadata from the document list and passes them to `collection.add()`:

```python
collection.add(
    documents=[doc["text"] for doc in exampleSourceDocuments],
    metadatas=[doc["metadata"] for doc in exampleSourceDocuments],
    ids=[str(i) for i in range(len(exampleSourceDocuments))]
)
```

### `queryVectorDb(query, source_type_filter=None)`

Includes `metadatas` in the returned fields and optionally applies a `where` filter:

```python
results = collection.query(
    query_texts=[query],
    n_results=5,
    where={"source_type": source_type_filter},  # optional
    include=["documents", "metadatas", "distances"]
)
```

### `create_context_with_sources(question)`

Pairs each retrieved document with its source tag:

```python
source_ref = f"[Source: {meta['source_title']}, {meta['section']} — {meta['source_url']}]"
context_parts.append(f"{doc}\n{source_ref}")
```

### `rag_query_with_citations(question)`

Instructs the LLM to cite sources for every fact in its answer, then returns both the answer and the raw metadata list for the source display footer.

---

## Extending the Knowledge Base

To add more documents:
1. Add new entries to `exampleSourceDocuments` in `sailing_documents_with_metadata.py`.
2. Delete the `chroma_db_data` directory (or the collection) so it is rebuilt on the next run.

To add new metadata fields, extend the `metadata` dict in each document and update the `print_sources()` function to display the new field.
