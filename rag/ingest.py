from rag.vector_store import VectorStore

vector_store = VectorStore()

def ingest_documents(texts):
    vector_store.add_texts(texts)
    return {"ingested": len(texts)}
