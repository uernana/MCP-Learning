# retriever.py

import pinecone
from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import re
from typing import List, Tuple, Optional
from sentence_transformers import SentenceTransformer

OPENAI_API_KEY = "your-openai-api-key"
PINECONE_API_KEY="your-pinecone-api-key"
PINECONE_INDEX="your-pinecone-index"

class Retriever:
    def __init__(self):
        # 1. Load embedding model (local)
        self.embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
        self.embedding_model = SentenceTransformer(self.embedding_model_name)

        # 2. Pinecone init
        self.pineconeClient = pinecone.Pinecone(api_key=PINECONE_API_KEY)
        self.pineconeIndex = self.pineconeClient.Index(PINECONE_INDEX)

        # 3. Stats
        self.totalVectorCount = self.pineconeIndex.describe_index_stats()["total_vector_count"]

    def get_embedding(self, inputText: str) -> List[float]:
        """
        Generate embeddings using Hugging Face SentenceTransformer
        """
        sanitizedText = inputText.replace("\n", " ")
        embedding = self.embedding_model.encode(
            sanitizedText,
            normalize_embeddings=True,  # IMPORTANT for cosine similarity
        )
        return embedding.tolist()

    def fetch_text_from_response(self, vectorId: str) -> Tuple[Optional[str], Optional[dict]]:
        response: FetchResponse = self.pineconeIndex.fetch(ids=[vectorId], namespace="")

        if vectorId in response.vectors:
            vectorData = response.vectors[vectorId]
            metadata = vectorData.metadata
            contentText = metadata.get("content") if metadata else None
            return contentText, metadata

        return None, None

    def run_similarity_search(
        self,
        queryText: str,
        min_similarity: Optional[float] = None,
        top_k: Optional[int] = None
    ) -> List[str]:

        min_similarity = min_similarity or float(os.getenv("RAG_MIN_SIMILARITY", "0.5"))
        top_k = top_k or int(os.getenv("RAG_TOP_K", "3"))

        queryEmbedding = self.get_embedding(queryText)

        searchResults = self.pineconeIndex.query(
            vector=queryEmbedding,
            top_k=top_k,
            include_metadata=False
        )

        vectorIdList = [
            match["id"]
            for match in searchResults.get("matches", [])
            if match.get("score", 0) >= min_similarity
        ]

        contextList = []
        for vectorId in vectorIdList:
            contentText, _ = self.fetch_text_from_response(vectorId)
            if contentText:
                contextList.append(contentText)

        return contextList
