# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from retriever_pinecone import Retriever
from fastapi_mcp import FastApiMCP
import uvicorn

app = FastAPI(
    title="MCP RAG Server",
    description="Retrieve academic research, study guides, and exam materials",
    version="1.0.0"
)

retriever = Retriever()

class SearchRequest(BaseModel):
    query: str

class DocumentSearchResponse(BaseModel):
    query: str
    results: List[str]

@app.post("/search_documents", response_model=DocumentSearchResponse, operation_id="search_relevant_documents")
async def search_documents(request: SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    results = retriever.run_similarity_search(request.query)
    return DocumentSearchResponse(query=request.query, results=results)

@app.get("/")
def root():
    return {"status": "ok"}

mcp = FastApiMCP(app)
mcp.mount_http()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
