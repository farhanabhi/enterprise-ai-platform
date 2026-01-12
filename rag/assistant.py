from rag.ingest import vector_store

def answer_question(question: str):
    context_chunks = vector_store.search(question, k=3)

    if not context_chunks:
        return "I do not have enough information to answer that yet."

    context = "\n".join(context_chunks)

    # Lightweight, rule-based generation to stay local & safe
    answer = f"Based on the available data:\n{context}"

    return answer
