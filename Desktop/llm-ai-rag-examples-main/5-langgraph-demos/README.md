# LangGraph Demos

A collection of demos showing how to build LLM-powered applications with LangGraph and Google Gemini.

## Installation

### 1. Create and activate a virtual environment

```bash
# Create the virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

The demos use Google Gemini models via LangChain. You need a Google API key:

```bash
# Windows
set GOOGLE_API_KEY=your-api-key-here

# macOS/Linux
export GOOGLE_API_KEY=your-api-key-here
```

### 4. Run a demo

```bash
python demo1-hello-world-graph.py
```

## Demo Overview

### demo1-hello-world-graph.py
Introduction to LangGraph basics. Builds a simple graph with multiple nodes and conditional edges that randomly selects a mood (happy, sad, neutral) and routes to different response nodes. No LLM is used — purely demonstrates graph structure, state management, and conditional routing.

### demo2.0-messages-invoke-llm.py
Shows how to construct a message history (SystemMessage, AIMessage, HumanMessage) and invoke a Google Gemini LLM directly using LangChain — without a graph. Demonstrates the basic pattern for interacting with a chat model.

### demo2.1-llm-in-graph.py
Wraps an LLM call inside a LangGraph graph. A single-node graph takes a message list as state, invokes Gemini, and appends the AI response. Demonstrates using the `add_messages` reducer to manage conversation history within a graph.

### demo3.0-tool-simple-demo.py
Introduces LangChain tool binding. Defines a weather tool that fetches real data from the Open-Meteo API and binds it to the LLM using `bind_tools()`. The LLM is invoked directly (no graph) to show how a model can request tool calls.

### demo3.1-tools-graph-bad.py
Demonstrates a manual (naive) approach to handling tool calls inside a LangGraph graph. The single node detects if the LLM requested a function call, executes the tool, and re-invokes the LLM with the tool result. Works but is verbose and hard to maintain.

### demo3.1-tools-graph-good.py
The improved version of the tool-calling graph using LangGraph's built-in `ToolNode` and `tools_condition`. This separates the LLM node from the tool-execution node and uses conditional edges to automatically route between them, resulting in cleaner and more maintainable code.

### demo4-basic-rag.py
A basic Retrieval-Augmented Generation (RAG) pipeline. Loads a fictional creature catalog into an in-memory ChromaDB vector store, retrieves relevant entries via similarity search, and passes them as context to Gemini to generate grounded answers. Demonstrates the retrieve-then-generate graph pattern.
