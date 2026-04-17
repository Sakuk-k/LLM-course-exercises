# Day 9 — LLM Web App Integration

A full-stack chat application that streams responses from the Gemini API in real time. The backend is a FastAPI server that proxies requests to Gemini; the frontend is a React app built with Vite.

---

## Architecture

```
Browser (React + Vite)
        │
        │  POST /chat  (non-streaming)
        │  POST /chat/stream  (SSE streaming)
        ▼
FastAPI Backend  (localhost:8000)
        │
        │  google.generativeai
        ▼
Gemini API  (gemini-2.5-flash-lite)
```

The backend exists for two reasons:
1. **API key security** — the Gemini key never leaves the server.
2. **Rate limiting** — the backend enforces a per-session request cap before forwarding to Gemini.

---

## How the application works

### Conversation history

The frontend maintains the full conversation in React state as a list of messages:

```js
[
  { role: 'user',      content: 'Hello!' },
  { role: 'assistant', content: 'Hi there!' },
  ...
]
```

Before every request, the frontend converts this list into the Gemini wire format (role `"assistant"` → `"model"`, `content` → `parts`) and sends the entire history to the backend. The backend builds a `contents` list from the received history plus the new user message and passes it to `model.generate_content()`. **There is no server-side session state** — the client is the single source of truth for history.

### Streaming toggle

The UI has a **Streaming** checkbox. Both modes hit the same Gemini model but use different endpoints and response handling:

| Mode | Endpoint | Response type |
|------|----------|---------------|
| On (default) | `POST /chat/stream` | Server-Sent Events (SSE) over `fetch` + `ReadableStream` |
| Off | `POST /chat` | Regular JSON response |

### Why `fetch` + `ReadableStream` instead of `EventSource`?

`EventSource` is the standard browser API for SSE — but it only supports `GET` requests. Because this app needs to send a JSON body (the message and history), it uses `fetch` with `response.body.getReader()` to consume the SSE stream manually over a `POST` request.

### Token usage and cost

After every response (streaming and non-streaming) the backend returns token counts and an estimated cost. These are displayed in the usage bar beneath the header.

---

## Communication protocol

### Non-streaming — `POST /chat`

**Request body:**

```json
{
  "message": "What is the capital of France?",
  "history": [
    { "role": "user",  "parts": [{ "text": "Hello!" }] },
    { "role": "model", "parts": [{ "text": "Hi! How can I help?" }] }
  ],
  "session_id": "session-abc123"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `message` | string | The new user message to send |
| `history` | array | Prior turns in Gemini format (may be empty `[]`) |
| `session_id` | string | Identifies the browser tab for rate limiting |

**Response body:**

```json
{
  "response": "The capital of France is Paris.",
  "usage": {
    "input_tokens": 42,
    "output_tokens": 9,
    "estimated_cost_usd": 0.000008
  }
}
```

---

### Streaming — `POST /chat/stream`

The request body is identical to `/chat`.

The response is a stream of Server-Sent Events with `Content-Type: text/event-stream`. Each event is a JSON object on a `data:` line, terminated by a blank line:

```
data: {"type": "text", "content": "The capital"}\n\n
data: {"type": "text", "content": " of France"}\n\n
data: {"type": "text", "content": " is Paris."}\n\n
data: {"type": "done", "usage": {"input_tokens": 42, "output_tokens": 9, "estimated_cost_usd": 0.000008}}\n\n
```

| Event type | Payload | When sent |
|------------|---------|-----------|
| `text` | `{ "type": "text", "content": "<token(s)>" }` | Once per chunk as Gemini generates tokens |
| `done` | `{ "type": "done", "usage": { ... } }` | Once, after the last token |

The frontend accumulates `text` chunks into the assistant message in real time and reads the `done` event to update the usage bar.

---

### Rate limiting

Each `session_id` is limited to **20 requests per 60 seconds** (in-memory, resets on server restart). Exceeding the limit returns:

```
HTTP 429  {"detail": "Rate limit exceeded. Try again in a moment."}
```

---

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- A [Gemini API key](https://aistudio.google.com/app/apikey)

### 1. Backend

```bash
cd 9-web-app-integration

# Copy and fill in the environment file
cp .env.example .env
# Edit .env and set GEMINI_API_KEY=<your key>

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Start the server
uvicorn backend.main:app --reload
```

The API is now running at `http://localhost:8000`. Open `http://localhost:8000/health` to verify.

### 2. Frontend

In a second terminal:

```bash
cd 9-web-app-integration/frontend

npm install
npm run dev
```

The app opens at `http://localhost:5173`.

---

## Project structure

```
9-web-app-integration/
├── .env.example              # Environment variable template
├── backend/
│   ├── main.py               # FastAPI app — /chat and /chat/stream endpoints
│   └── requirements.txt      # Python dependencies
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx               # Root component — state, fetch logic, streaming
        ├── main.jsx
        ├── index.css
        └── components/
            ├── ChatInput.jsx     # Textarea + send button
            ├── MessageList.jsx   # Renders the conversation bubbles
            └── UsageBar.jsx      # Token count and cost display
```
