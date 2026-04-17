# --- RETRIEVAL (the "R" in RAG) ---
# NearestNeighbors is a k-nearest-neighbors (kNN) search algorithm from scikit-learn.
# It builds an in-memory index over embedding vectors so we can quickly find the
# documents whose embeddings are closest (most similar) to a query embedding.
# We use it here as a simple vector store / retrieval engine.
from sklearn.neighbors import NearestNeighbors

# NumPy provides efficient n-dimensional array operations.
# Used here to convert embedding tensors into plain NumPy arrays that
# NearestNeighbors can consume (it expects array-like input).
import numpy as np

# --- EMBEDDING MODEL ---
# SentenceTransformer (from the `sentence-transformers` library) wraps a
# transformer model to produce vector representations/embeddings for sentences/paragraphs.
# Calling model.encode(texts) returns one embedding vector per text.
# These embeddings capture semantic meaning, so texts with similar meaning
# end up close together in vector space — which is what makes retrieval work.
from sentence_transformers import SentenceTransformer

# --- GENERATION ---
#  Huggingface provided AutoModelForSeq2SeqLM loads a sequence-to-sequence language 
#   model (e.g. T5, FLAN-T5).
#   Seq2Seq models take an input sequence (our prompt with context + question) and
#   produce an output sequence (the answer). This is different from causal/decoder-only
#   models (like GPT) which only predict the next token in a single sequence.
#   FLAN-T5 was instruction-tuned, making it good at following prompts like
#   "Answer with facts from the context."
#
# AutoTokenizer loads the matching tokenizer for the model.
#   A tokenizer converts raw text into token IDs (integers) that the model understands,
#   and converts token IDs back into human-readable text. Every model has its own
#   vocabulary, so the tokenizer must match the model.
from transformers import AutoModelForSeq2SeqLM,  AutoTokenizer


def load_data_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        documents = [line.strip() for line in f if line.strip()]
    return documents

def create_embeddings(documents, model):
    embeddings = model.encode(documents, convert_to_tensor=True)
    return np.array(embeddings)

def build_index(embeddings):
    index = NearestNeighbors(n_neighbors=5, metric='euclidean')  # or 'cosine'
    # .fit() builds the search index from the embedding vectors.
    # It organizes all document embeddings into a data structure optimized for
    # nearest-neighbor lookup. After fitting, we can query the index with a new
    # embedding and it will efficiently find the k closest document embeddings.
    # No training happens here — "fit" is scikit-learn's convention for
    # "process this data and prepare for queries."
    index.fit(embeddings)
    return index

def retrieve_documents(query, model, index, documents, k=1):
    query_embedding = model.encode([query], convert_to_tensor=False)
    distances, indices = index.kneighbors(query_embedding, n_neighbors=k)
    print(f"Distances: {distances}, Indices: {indices}")
    return [documents[idx] for idx in indices[0]]

def generate_answer(query, retrieved_docs, tokenizer, model):
    """Generate an answer using the retrieved documents as context."""

    # Build the prompt: combine the retrieved context with the question
    context = "\n".join(retrieved_docs)
    prompt = f"Context: {context}\nAnswer with facts from the context. Here is the question: {query}\nAnswer: "

    # Tokenize the prompt — converts raw text into token IDs the model understands.
    #   return_tensors="pt": return as PyTorch tensors (required by model.generate())
    #   truncation=True:     cut off if prompt exceeds model's max length (512 for T5)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)    
    #print("Tokenized prompt input IDs:", inputs.input_ids)
    print("Tokenized prompt attention mask:", inputs.attention_mask)

    # Generate the answer.
    # model.generate() runs the full generation loop internally and returns
    # a tensor of token IDs representing the generated answer.
    #   inputs.input_ids:      the tokenized prompt
    #   attention_mask:        tells the model which tokens are real (1) vs padding (0)
    #   max_length=150:        stop after 150 tokens
    #   do_sample=False:       greedy decoding — always pick the most likely token (no randomness)
    output_ids = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=150,
        do_sample=False,
    )

    # Decode the generated token IDs back into a readable text string.
    # skip_special_tokens=True removes tokens like <pad>, </s> from the output.
    answer = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return answer

def main():
    # Load data
    print("Loading data...")
    data_file = "./data.txt"
    documents = load_data_from_file(data_file)
    print(f"Loaded {len(documents)} documents.")
    if not documents:
        print("No documents found in the file.")
        return
    
    print("Loading retriever model...")
    retriever_model = SentenceTransformer('all-MiniLM-L6-v2')

    # Create embeddings and index
    embeddings = create_embeddings(documents, retriever_model)
    index = build_index(embeddings)         
    print("Index built successfully.")
    
    # https://huggingface.co/google/flan-t5-base
    model_name = "google/flan-t5-base"
    
    print(f"Loading generator model: {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)    
    gen_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    print("Generator model loaded successfully.")

    # Example query
    query = "What materials should I use to build a playhouse outside for my children?"
    

    print(f"Query: {query}")
    # Retrieve relevant documents
    retrieved_docs = retrieve_documents(query, retriever_model, index, documents, k=1)
    print(f"Retrieved document: {retrieved_docs}")

    answer = generate_answer(query, retrieved_docs, tokenizer, gen_model)
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()