# RAG System with Gemini

This repository contains a simple implementation of a **Retrieval-Augmented Generation (RAG)** system using Google's **Gemini API** and `sentence-transformers`. This example demonstrates how to combine a retrieval component with an online large language model (LLM) to generate more informed and contextually relevant answers.

---

## How It Works

This RAG system operates in a few key steps:

1.  **Setup and Initialization**: The code sets up the necessary libraries and configures access to the Gemini API using an environment variable for your API key. It also initializes a `SentenceTransformer` model (`all-MiniLM-L6-v2`) to convert text into numerical representations called embeddings.
2.  **Knowledge Base and Embeddings**: A small, in-memory **knowledge base** (a list of sentences) is defined. Each sentence in this base is transformed into an embedding. These embeddings capture the semantic meaning of the text, allowing for efficient similarity comparisons.
3.  **Context Retrieval**: When a question is posed, it's also converted into an embedding. The system then calculates the **cosine similarity** between the question's embedding and all embeddings in the knowledge base. The sentences most similar to the question are retrieved and used as **context**.
4.  **Gemini API Interaction**: The retrieved context and the original question are combined into a single **prompt**. This prompt is then sent to the **Gemini 2.0 Flash LLM**.
5.  **Answer Generation**: Gemini generates an answer based on the provided context and question, ensuring the response is relevant and informed by the knowledge base.

---

## Getting Started

Follow these steps to set up and run the RAG system:

### Prerequisites

* Python 3.8 or higher
* Access to the Gemini API. You'll need an **API key**. Read more here: [text](https://ai.google.dev/gemini-api/docs/api-key)

### Installation

1.  **Create a virtual environment**:
    It is recommended to use a virtual environment to keep dependencies isolated.
    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment**:
    * **Linux/macOS**:
        ```bash
        source venv/bin/activate
        ```
    * **Windows (Command Prompt)**:
        ```bash
        venv\Scripts\activate.bat
        ```
    * **Windows (PowerShell)**:
        ```powershell
        venv\Scripts\Activate.ps1
        ```

3.  **Install dependencies**:
    This project uses a `requirements.txt` file to manage its dependencies.
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Set your Gemini API Key**:
    The system requires your Gemini API key to be set as an environment variable named `GEMINI_API_KEY`.
    
    * **Linux/macOS**:
        ```bash
        export GEMINI_API_KEY="YOUR_API_KEY"
        ```
    * **Windows (Command Prompt)**:
        ```bash
        set GEMINI_API_KEY="YOUR_API_KEY"
        ```
    * **Windows (PowerShell)**:
        ```powershell
        $env:GEMINI_API_KEY="YOUR_API_KEY"
        ```
    
    Replace `"YOUR_API_KEY"` with your actual Gemini API key.

### Running the Code

After setting up your API key, you can run the main script:

```bash
python gemini-rag-hello-world.py
```
(Assuming the provided code is saved as `gemini-rag-hello-world.py`)

The script will then execute the example query and print the question and the generated answer to your console.

---

## Customization

You can easily customize this RAG system:

* **Knowledge Base**: Modify the `knowledge_base` list in the code to include your own domain-specific information. For larger knowledge bases, consider loading data from a file (e.g., CSV, JSON, or a database).
* **Top-K Context**: Adjust the `top_k` parameter in the `retrieve_context` function to control how many of the most similar knowledge base entries are used as context for the LLM.
* **Gemini Model**: You can experiment with different Gemini models if available and suitable for your use case by changing `'gemini-2.0-flash'` in `genai.GenerativeModel()`.

---