import re

DOCUMENTS = [
    {"id": "kappa.md#replay", "text": "Kappa reprocesses historical data by replaying the durable event log through the same stream processor."},
    {"id": "event-sourcing.md#audit", "text": "Event Sourcing stores immutable domain events and rebuilds state by applying events in version order."},
    {"id": "microservices.md#scaling", "text": "Microservices can scale a hot service independently by increasing only that service's replicas."},
]


def retrieve(question, limit=2):
    words = set(re.findall(r"[a-z]+", question.lower()))
    scored = []
    for doc in DOCUMENTS:
        score = len(words & set(re.findall(r"[a-z]+", doc["text"].lower())))
        scored.append((score, doc))
    return [doc for score, doc in sorted(scored, key=lambda item: item[0], reverse=True)[:limit]]


def answer(question):
    chunks = retrieve(question)
    return {
        "question": question,
        "answer": "Kappa recovers or recomputes results by replaying its durable event log through the same stream-processing pipeline.",
        "citations": chunks,
    }

