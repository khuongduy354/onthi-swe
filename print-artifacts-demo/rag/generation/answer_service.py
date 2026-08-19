from rag.generation.prompt_builder import build_prompt
from rag.retrieval.retriever import retrieve


def answer(question):
    chunks = retrieve(question)
    build_prompt(question, chunks)  # boundary where a hosted/local LLM would be called
    return {
        "question": question,
        "answer": "Kappa recovers or recomputes results by replaying its durable event log through the same stream-processing pipeline.",
        "citations": chunks,
    }

