# 1. What we are building (goal)

A **Retrieval-Augmented Generation (RAG)** system that:

* Serves **humans** via HTTP (web, app, UI)
* Serves **LLMs / agents** via MCP
* Supports:

  * document ingestion
  * embedding
  * retrieval
  * reasoning
  * streaming answers
* Is **scalable, observable, and secure**

---

# 2. High-level architecture (bird’s-eye view)

```
                ┌───────────────┐
                │   Web / UI    │
                │ (Gradio, FE)  │
                └───────┬───────┘
                        │ HTTP / WS
                        ▼
                ┌──────────────────┐
                │     FastAPI      │  ← API Gateway
                │ (Auth, Upload,   │
                │  Sessions)       │
                └───────┬──────────┘
                        │ MCP Client
                        ▼
                ┌──────────────────┐
                │    FastMCP       │  ← AI Tool Server
                │ (RAG tools)      │
                └───────┬──────────┘
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 ┌────────────┐  ┌────────────┐  ┌────────────┐
 │ Vector DB  │  │  Document  │  │   LLM API  │
 │ (FAISS,    │  │  Store     │  │ (GPT/Claude)│
 │ Qdrant)    │  │ (S3, FS)   │  └────────────┘
 └────────────┘  └────────────┘
```

---

# 3. Clear separation of responsibilities (IMPORTANT)

## FastAPI = **Human-facing layer**

Handles:

* Authentication (JWT / OAuth)
* File uploads (PDF, DOCX, TXT)
* User sessions
* Rate limiting
* Streaming responses (SSE / WebSocket)
* Monitoring & logging

**FastAPI never reasons.**
It *orchestrates*.

---

## FastMCP = **LLM-facing tool layer**

Handles:

* RAG tools
* Structured context
* Search / retrieve / embed
* Deterministic tool APIs for agents

**FastMCP never handles auth or UI.**
It *empowers reasoning*.

---

# 4. RAG pipeline (core logic)

### The classic RAG loop:

```
User query
   ↓
Embedding
   ↓
Vector search
   ↓
Relevant chunks
   ↓
Prompt + context
   ↓
LLM answer
```

In this architecture:

* **FastMCP owns this logic**
* **FastAPI calls it**

---

# 5. FastMCP: RAG tool design

### MCP tools (example)

```python
# mcp_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("rag-tools")

@mcp.tool()
async def embed(text: str) -> list[float]:
    ...

@mcp.tool()
async def retrieve(query: str, k: int = 5) -> list[dict]:
    ...

@mcp.tool()
async def answer(query: str) -> str:
    """
    1. Embed query
    2. Retrieve top-k chunks
    3. Build prompt
    4. Call LLM
    """
    ...
```

Each tool:

* Has **strict input/output schema**
* Is **LLM-safe**
* Is **testable in isolation**

---

# 6. FastAPI: orchestration layer

### Upload documents

```python
@app.post("/documents/upload")
async def upload(file: UploadFile):
    # save to storage
    # call MCP: chunk + embed + store
    ...
```

### Ask a question

```python
@app.post("/query")
async def query_rag(q: str):
    async with mcp_session() as mcp:
        result = await mcp.call_tool("answer", {"query": q})
        return result
```

### Streaming answers (recommended)

```python
@app.get("/query/stream")
async def stream(q: str):
    async def generator():
        async with mcp_session() as mcp:
            async for chunk in mcp.stream_tool("answer", {"query": q}):
                yield f"data: {chunk}\n\n"
    return StreamingResponse(generator(), media_type="text/event-stream")
```

---

# 7. Data storage layout

## Document Store (raw data)

```
/documents
  ├── doc_id
  │    ├── original.pdf
  │    ├── chunks.json
```

* S3 / MinIO / filesystem
* Immutable

---

## Vector Store (semantic search)

Stores:

* chunk embedding
* metadata (doc_id, page, section)

Options:

* FAISS (local)
* Qdrant
* Weaviate
* Pinecone

---

## Memory / State (optional)

* Redis
* PostgreSQL

Used for:

* conversation history
* session memory
* agent state

---

# 8. Request lifecycle (step-by-step)

### Query request

```
1. User → FastAPI /query
2. FastAPI validates & authenticates
3. FastAPI → MCP answer tool
4. MCP:
   a. embed query
   b. vector search
   c. assemble context
   d. call LLM
5. MCP returns structured answer
6. FastAPI streams / returns response
```

---

# 9. Why MCP is PERFECT for RAG

Traditional RAG problems:

* Loose prompts
* Tool chaos
* Hard to debug
* No contracts

MCP fixes this by:

* Enforcing **tool schemas**
* Making context **explicit**
* Allowing **agent-level reasoning**
* Supporting **Claude Desktop / agents natively**

---

# 10. Deployment architecture (realistic)

```
docker-compose
├── fastapi-gateway
├── mcp-rag-server
├── vector-db
├── redis (optional)
└── nginx
```

Scaling:

* FastAPI → horizontal scale
* MCP → scale by tool load
* Vector DB → separate service

---

# 11. Security boundaries (VERY IMPORTANT)

| Layer     | Exposure           |
| --------- | ------------------ |
| FastAPI   | Public             |
| MCP       | Private (internal) |
| Vector DB | Private            |
| LLM keys  | MCP only           |

🚫 Never expose MCP directly to the internet.

---


