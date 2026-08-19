from rag.infrastructure.vector_store import search


def retrieve(question, limit=2):
    return search(question, limit)
