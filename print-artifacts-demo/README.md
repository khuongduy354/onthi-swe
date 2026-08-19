# Lightweight demos for print artifacts

Run with only Python standard library:

```bash
cd print-artifacts-demo
python server.py
```

Open http://localhost:8090. The demo contains small, runnable examples for
Micro-Frontends, JAMstack, local RAG, an offline Agent planner, Event Sourcing,
Event-Driven Architecture, and Kappa reporting.

Each example is separated by architecture responsibility rather than placed in
one file: RAG has ingestion/retrieval/generation; Agent has model/core/tools/policy;
Event Sourcing has domain/application/event-store/projection; EDA has contracts,
producer, broker and consumer; Kappa has producer, event log, stream processor,
serving storage and report API.

Container deployment:

```bash
docker build -t architecture-print-demo .
docker run -d --name architecture-print-demo -p 8090:8090 architecture-print-demo
docker ps --filter name=architecture-print-demo
```
