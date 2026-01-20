# MCP RAG Server (FastAPI + Pinecone + Hugging Face + FastMCP)

A **Retrieval-Augmented Generation (RAG) backend** built with **FastAPI**, **Pinecone**, and **Hugging Face embeddings**, exposed as both a **REST API** and an **MCP (Model Context Protocol) server**.

This service retrieves semantically relevant document chunks from a vector database and is designed to be consumed by:

* Web applications
* AI agents
* Claude Desktop via MCP
* Other LLM systems

---

## 🚀 Features

* 🔍 Semantic search using Hugging Face embeddings
* 🧠 Vector similarity search with Pinecone
* ⚡ FastAPI REST interface
* 🔌 MCP-compatible (Model Context Protocol)
* 📦 Clean, modular retriever design
* 🌐 Ready for AI agent integration

---

## 📁 Project Structure

```
.
├── main.py                  # FastAPI + MCP server
├── retriever.py    # Retriever logic
├── test_file.py                # (Optional) document ingestion
├── .env                     # Environment variables
├── README.md
```

---

## 🧠 Retriever Logic

The `Retriever` class is responsible for:

* Loading a **local Hugging Face embedding model**
* Connecting to **Pinecone**
* Running **cosine similarity search**
* Fetching original document text from metadata

### Embedding model used

```
sentence-transformers/all-MiniLM-L6-v2
```

* Dimension: **384**
* Metric: **cosine similarity**
* Runs locally (no OpenAI API required)

---

## ⚙️ Requirements

### Python

* Python **3.9+**

### Dependencies

```bash
pip install fastapi uvicorn pinecone-client sentence-transformers python-dotenv fastapi-mcp
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
PIPECONE_API_KEY=your_pinecone_api_key
PIPECONE_INDEX=your_index_name

RAG_MIN_SIMILARITY=0.5
RAG_TOP_K=3
```

---

## 📦 Pinecone Setup (Required)

The Pinecone index **must match the embedding dimension**.

For `all-MiniLM-L6-v2`:

* Dimension: **384**
* Metric: **cosine**

Create the index once:

```python
import pinecone

pc = pinecone.Pinecone(api_key="YOUR_API_KEY")

pc.create_index(
    name="your-index-name",
    dimension=384,
    metric="cosine"
)
```

---

## 📥 Ingest Test Data (Required Before Search)

The retriever assumes documents are already indexed.

Example `ingest.py`:

```python
import uuid
from retriever_pinecone import Retriever

retriever = Retriever()

text = """
FastAPI is a modern, high-performance Python web framework for building APIs.
It is built on Starlette and Pydantic.
"""

embedding = retriever.get_embedding(text)

retriever.pineconeIndex.upsert([
    {
        "id": str(uuid.uuid4()),
        "values": embedding,
        "metadata": {
            "content": text,
            "source": "example"
        }
    }
])

print("Document indexed")
```

Run:

```bash
python ingest.py
```

---

## ▶️ Run the Server

```bash
python main.py
```

Server will start at:

```
http://localhost:8001
```

---

## 🧪 Test the API

### Health Check

```http
GET /
```

Response:

```json
{
  "status": "ok"
}
```

---

### Semantic Search Endpoint

```http
POST /search_documents
```

Request body:

```json
{
  "query": "What is FastAPI?"
}
```

Response:

```json
{
  "query": "What is FastAPI?",
  "results": [
    "FastAPI is a modern, high-performance Python web framework..."
  ]
}
```

---

## 📖 Swagger UI

Open in browser:

```
http://localhost:8001/docs
```

This allows you to:

* Inspect schemas
* Test endpoints interactively
* Debug requests easily

---

## 🔌 MCP Integration

The server is MCP-enabled via:

```python
mcp = FastApiMCP(app)
mcp.mount_http()
```

This exposes the endpoint as an MCP tool:

```
search_relevant_documents(query: string)
```

### Example MCP Usage (Claude Desktop)

1. Open **Settings → Developer → MCP**
2. Add server:

   ```
   http://localhost:8001
   ```
3. Ask:

   > Search relevant documents about FastAPI

Claude will call the MCP tool automatically.



