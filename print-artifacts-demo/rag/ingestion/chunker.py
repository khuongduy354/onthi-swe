def chunk(document, size=120):
    """Split source text before embedding/indexing."""
    words = document.split()
    return [" ".join(words[index:index + size]) for index in range(0, len(words), size)]

