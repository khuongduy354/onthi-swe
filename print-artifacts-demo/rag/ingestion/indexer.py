from rag.data.documents import DOCUMENTS
from rag.ingestion.chunker import chunk


def build_index():
    """Offline stand-in for an embedding/vector indexing job."""
    return [{"id": doc["id"], "text": part} for doc in DOCUMENTS for part in chunk(doc["text"])]

