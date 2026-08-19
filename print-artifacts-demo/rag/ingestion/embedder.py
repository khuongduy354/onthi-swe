from rag.retrieval.tokenizer import tokens


def embed(text):
    """Deterministic offline embedding used by the demo."""
    return tokens(text)

