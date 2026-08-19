def build_prompt(question, chunks):
    context = "\n".join(f"[{chunk['id']}] {chunk['text']}" for chunk in chunks)
    return f"Answer only from this context:\n{context}\nQuestion: {question}"

