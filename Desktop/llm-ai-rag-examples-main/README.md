# RAG Demos for LLMs

A collection of progressively more advanced demos exploring **Retrieval-Augmented Generation (RAG)** concepts for Large Language Models. Each demo lives in its own folder with its own README and `requirements.txt`.

---

## Demos

| Folder | Description |
|--------|-------------|
| [`1-local-hello-worldrag`](./1-local-hello-worldrag/) | RAG hello world – a minimal local RAG pipeline in pure Python |
| [`2-gemini-rag-hello-world`](./2-gemini-rag-hello-world/) | RAG with Google Gemini API and `sentence-transformers` |
| [`3-vectordb-intro`](./3-vectordb-intro/) | Introduction to vector databases using ChromaDB |
| [`4-rag-with-vectordb`](./4-rag-with-vectordb/) | Full RAG pipeline combining ChromaDB and Gemini |
| [`5-langchain-rag-intro`](./5-langchain-rag-intro/) | RAG with the LangChain framework and Milvus as vector store |
| [`6-langchain-different-llm-providers`](./6-langchain-different-llm-providers/) | Swapping LLM providers (Azure OpenAI, Mistral, Gemini) via LangChain |
| [`llama3-base`](./llama3-base/) | Running Llama 3.1 locally from Hugging Face with streaming output |

---

## Setup

Each demo uses the shared `venv` in the project root.

**1. Create the virtual environment** (only needed once):

```bash
python -m venv venv
```

**2. Activate it:**

```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

Once activated you'll see `(venv)` at the start of your prompt.

**3. Install dependencies for a demo:**

```bash
cd <demo-folder>
pip install -r requirements.txt
```

**4. Run the demo** – check the README inside the folder for the exact command. Most demos use:

```bash
python main.py
```

---

## Example

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows
cd 4-rag-with-vectordb
pip install -r requirements.txt
python main.py
```
