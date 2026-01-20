from retriever_pinecone import Retriever
import uuid

retriever = Retriever()

text = open("your file path").read()

embedding = retriever.get_embedding(text)

retriever.pineconeIndex.upsert([
    {
        "id": str(uuid.uuid4()),
        "values": embedding,
        "metadata": {
            "content": text,
            "source": "test_data.txt"
        }
    }
])

retriever = Retriever()
results = retriever.run_similarity_search("What is FastAPI?")
print(results)
