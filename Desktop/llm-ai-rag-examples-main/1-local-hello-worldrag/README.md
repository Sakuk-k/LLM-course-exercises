# RAG Hello World

This project demonstrates a simple Retrieval-Augmented Generation (RAG) workflow using Python. Everything runs locally — no API keys or cloud services needed.

## Files

- `rag-hello-world.py`: Main script implementing the RAG pipeline.
- `data.txt`: Custom knowledge base — each line is a "document" the model can retrieve from.
- `requirements.txt`: Python dependencies.

## Requirements

- Python 3.8+

To create and activate a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

Then install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python rag-hello-world.py
```

## How It Works

The script implements a minimal RAG pipeline with three stages: **Embed, Retrieve, Generate**.

### 1. Load the Knowledge Base

The script reads `data.txt` line by line. Each non-empty line becomes a "document" in the knowledge base.

### 2. Embed the Documents

Each document is converted into a dense vector (embedding) using the [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) model from the `sentence-transformers` library. These vectors capture semantic meaning — similar texts end up close together in vector space.

The embeddings are then loaded into a **NearestNeighbors** index (from scikit-learn), which allows fast similarity search.

### 3. Retrieve Relevant Documents

When a query comes in, it is also embedded into a vector using the same model. The NearestNeighbors index finds the document(s) whose embeddings are closest to the query embedding (using Euclidean distance). This is the **Retrieval** step — finding the most relevant context.

### 4. Generate an Answer

The retrieved document(s) and the original query are combined into a prompt and passed to [google/flan-t5-base](https://huggingface.co/google/flan-t5-base), a sequence-to-sequence language model. The prompt instructs the model to answer using facts from the provided context.

The generation process:
1. **Tokenize** — convert the prompt text into token IDs the model understands
2. **Generate** — the model produces output token IDs (using greedy decoding)
3. **Decode** — convert the output token IDs back into readable text

### 5. Display the Answer

The generated answer is printed to the console.

## Key Libraries

| Library | Role | Used For |
|---------|------|----------|
| `sentence-transformers` | Embedding model | Converting text into semantic vectors |
| `scikit-learn` | Vector search | NearestNeighbors index for finding similar documents |
| `transformers` | Language model | Loading FLAN-T5 model and tokenizer for answer generation |
| `numpy` | Array operations | Converting embedding tensors to arrays for scikit-learn |
| `torch` | Tensor framework | Required backend for the transformer models |

## Why RAG?

Without RAG, a language model can only answer from what it learned during training. RAG adds a retrieval step that gives the model access to external, up-to-date, or domain-specific data — so it can answer questions about information it was never trained on.
