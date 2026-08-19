from rag.ingestion.embedder import embed
from rag.ingestion.indexer import build_index


def similarity(left, right):
    union = left | right
    return len(left & right) / len(union) if union else 0


def search(query, limit=2):
    query_vector = embed(query)
    scored = [(similarity(query_vector, embed(chunk["text"])), chunk) for chunk in build_index()]
    return [chunk for _, chunk in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]

