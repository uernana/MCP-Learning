# 🌦 MCP Weather Assistant (Gradio + FastMCP + GPT-4o-mini)

This project demonstrates how to build a **Model Context Protocol (MCP)** application using:

* **FastMCP** as a tool server
* **OpenAI GPT-4o-mini** as the LLM client
* **Gradio** as a web UI
* **stdio-based MCP transport** (no HTTP server needed)

The assistant can answer weather-related questions by **dynamically calling MCP tools** exposed by a FastMCP server.

---

## ✨ Features

* ✅ Model Context Protocol (MCP) compliant
* 🔧 Tool calling via FastMCP
* 🤖 LLM orchestration using GPT-4o-mini
* 🖥 Interactive Gradio chatbot UI
* ⚡ Async, non-blocking architecture
* 🧩 Clean separation: **Server / Client / UI**

---

## 🧠 Architecture Overview

```
┌────────────────────┐
│     Gradio UI      │
│ (Chatbot frontend) │
└─────────┬──────────┘
          │ user query
          ▼
┌────────────────────┐
│  MCP Gradio Client │
│  (client.py logic)│
└─────────┬──────────┘
          │
          │ 1. Ask LLM (GPT-4o-mini)
          │ 2. Decide tool call
          ▼
┌────────────────────┐
│   OpenAI API       │
│ (GPT-4o-mini)      │
└─────────┬──────────┘
          │ function_call
          ▼
┌────────────────────┐
│  MCP ClientSession │
│ (stdio transport)  │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ FastMCP Server     │
│ (server.py)        │
│ Weather tools      │
└────────────────────┘
```

### Key Idea

* The **LLM never fetches weather directly**
* It **decides** whether to call a tool
* MCP executes the tool
* Results are returned to the LLM
* The LLM produces the final answer

---

## 📁 Project Structure

```
.
├── server.py        # FastMCP tool server (weather tools)
├── mcp_gradio_app.py           # Gradio + MCP client
├── .env             # OpenAI API key
├── pyproject.toml   # uv / Python dependencies
├── assets   # uv / Python dependencies
└── README.md
```

---

## 🔧 Prerequisites

### 1. Python

* Python **3.10+** recommended

Check:

```bash
python --version
```

---

### 2. uv (recommended)

This project uses **uv** for fast dependency management.

Install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or via pip:

```bash
pip install uv
```

---

### 3. OpenAI API Key

Create a `.env` file:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

---

## 📦 Dependencies

Main libraries used:

* `mcp`
* `gradio`
* `openai`
* `httpx`
* `python-dotenv`

Install everything:

```bash
uv add mcp gradio openai httpx python-dotenv
```

or (if not using uv):

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

### 1️⃣ Start the Gradio app (auto-starts MCP server)

```bash
python app.py
```

You should see:

```
Connected MCP tools: ['get_alerts', 'get_forecast']
Running on http://127.0.0.1:7860
```

Open your browser at:

👉 **[http://localhost:7860](http://localhost:7860)**

---

### 2️⃣ Ask questions like

* `What are the weather alerts in Washington?`
* `Get forecast for latitude 40.7 longitude -74.0`
* `Is there any severe weather in California?`

The LLM will automatically decide when to call MCP tools.

---

## 🔍 How Tool Calling Works (Important)

1. User enters a question
2. GPT-4o-mini receives:

   * user query
   * MCP tool schemas
3. GPT chooses:

   * ❌ answer directly
   * ✅ or call a tool (e.g. `get_alerts`)
4. MCP executes the tool
5. Tool result is fed back to GPT
6. GPT produces final response

✔ Fully aligned with MCP design philosophy.

---

## 🧪 Debugging Tips

### UI stuck on “processing…”

* Ensure:

  * MCP server started correctly
  * You are using **AsyncOpenAI**
  * No blocking calls inside Gradio handlers

### Gradio error about message format

Make sure Chatbot uses:

```python
gr.Chatbot(type="messages")
```

And messages look like:

```python
{"role": "user", "content": "..."}
{"role": "assistant", "content": "..."}
```

---

## Reference

https://modelcontextprotocol.io/docs
