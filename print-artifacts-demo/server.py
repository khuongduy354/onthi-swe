import html
import json
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from agent.agent import run as run_agent
from event_driven.broker import EVENT_LOG, PROCESSED, publish
from event_sourcing.model import EVENTS, append as append_event, project
from kappa.pipeline import RAW_EVENTS, aggregate, append as append_stream
from rag.retriever import answer as rag_answer

ROOT = Path(__file__).parent


def layout(title, subtitle, content):
    return f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'>
    <title>{html.escape(title)}</title><link rel='stylesheet' href='/static/styles.css'></head><body>
    <header><h1>Software Architecture Lab</h1><div class='nav'><a href='/'>Home</a><a href='/rag'>RAG</a><a href='/event-sourcing/input'>Events</a><a href='/kappa/report'>Kappa</a></div></header>
    <main><h2>{html.escape(title)}</h2><p class='lead'>{html.escape(subtitle)}</p>{content}</main></body></html>"""


def table(headers, rows):
    head = "".join(f"<th>{html.escape(str(x))}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(x))}</td>" for x in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


class Handler(BaseHTTPRequestHandler):
    def send_html(self, body, status=200):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/static/styles.css":
            data = (ROOT / "static/styles.css").read_bytes()
            self.send_response(200); self.send_header("Content-Type", "text/css"); self.end_headers(); self.wfile.write(data); return
        if path.startswith("/fragments/"):
            name = Path(path).name
            body = (ROOT / "microfrontends" / name).read_text()
            self.send_html(body); return
        routes = {
            "/": self.home,
            "/mfe/account": lambda: self.mfe_single("account"),
            "/mfe/search": lambda: self.mfe_single("search"),
            "/mfe/shell": self.mfe_shell,
            "/jamstack": self.jamstack,
            "/rag": self.rag,
            "/agent": self.agent,
            "/event-sourcing/input": self.es_input,
            "/event-sourcing/list": self.es_list,
            "/event-driven/input": self.eda_input,
            "/kappa/input": self.kappa_input,
            "/kappa/report": self.kappa_report,
            "/kappa/raw": self.kappa_raw,
        }
        if path not in routes:
            self.send_html(layout("Not found", path, ""), 404); return
        self.send_html(routes[path]())

    def do_POST(self):
        size = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(size).decode())
        path = urlparse(self.path).path
        if path == "/event-sourcing/input":
            append_event("StudentAdded", {"id": form.get("id", ["SV002"])[0], "name": form.get("name", ["Student"])[0]})
            self.redirect("/event-sourcing/list"); return
        if path == "/event-driven/input":
            publish({"eventId": str(uuid.uuid4())[:8], "type": "ReservationCreated", "hotelId": form.get("hotelId", ["H01"])[0]})
            self.redirect("/event-driven/input"); return
        if path == "/kappa/input":
            append_stream({"eventId": str(uuid.uuid4())[:8], "category": form.get("category", ["Hotel"])[0], "amount": int(form.get("amount", ["100"])[0]), "time": "now"})
            self.redirect("/kappa/report"); return
        self.send_html("not found", 404)

    def redirect(self, location):
        self.send_response(303); self.send_header("Location", location); self.end_headers()

    def home(self):
        cards = [("Micro-Frontends", "/mfe/shell"), ("JAMstack", "/jamstack"), ("RAG", "/rag"), ("LLM Agent", "/agent"), ("Event Sourcing", "/event-sourcing/input"), ("Event-Driven", "/event-driven/input"), ("Kappa", "/kappa/report")]
        content = "<div class='grid'>" + "".join(f"<div class='card'><span class='tag'>Runnable demo</span><h3>{name}</h3><p><a href='{url}'>Open interface →</a></p></div>" for name, url in cards) + "</div>"
        return layout("Architecture demos", "Small examples used to produce exam print artifacts.", content)

    def mfe_single(self, name):
        fragment = (ROOT / "microfrontends" / f"{name}.html").read_text()
        return layout(f"{name.title()} Micro-Frontend", "This interface can run and be deployed independently.", fragment)

    def mfe_shell(self):
        content = """<div class='flow'><span class='node'>App Shell</span><span class='arrow'>loads →</span><span class='node'>Independent UI fragments</span></div>
        <div class='grid'><div id='account'></div><div id='search'></div><div id='report'></div></div>
        <script>for (const n of ['account','search','report']) fetch('/fragments/'+n+'.html').then(r=>r.text()).then(x=>document.getElementById(n).innerHTML=x)</script>"""
        return layout("Composed Micro-Frontend system", "App Shell composes three independently owned interface fragments at runtime.", content)

    def jamstack(self):
        built = (ROOT / "jamstack/dist/index.html").read_text()
        content = "<div class='flow'><span class='node'>Git/CMS</span><span class='arrow'>→</span><span class='node'>Build</span><span class='arrow'>→</span><span class='node'>Static HTML</span><span class='arrow'>→</span><span class='node'>CDN</span></div>" + built
        return layout("JAMstack static site", "Markup was generated at build time; dynamic data would be fetched from an API.", content)

    def rag(self):
        result = rag_answer("How does Kappa recover and recompute reports?")
        citations = "".join(f"<div class='citation'><b>{c['id']}</b><br>{c['text']}</div>" for c in result["citations"])
        content = f"<div class='card'><label>Question</label><input value='{result['question']}'><h3>Grounded answer</h3><p>{result['answer']}</p><h3>Retrieved top-2 citations</h3>{citations}</div>"
        return layout("Local RAG interface", "Keyword retrieval over local documents; answer includes the retrieved sources.", content)

    def agent(self):
        result = run_agent("Check two room-nights and calculate the total")
        steps = "".join(f"<div class='trace'><b>Tool: {s['tool']}</b><br><span class='muted'>args={s['args']}</span><br>result={s['result']}</div>" for s in result["steps"])
        content = f"<div class='card'><label>Task</label><input value='{result['task']}'><h3>Agent execution</h3>{steps}<p class='ok'>Final answer: {result['answer']}</p></div>"
        return layout("LLM-based Agent pattern", "Offline MockLLMPlanner chooses tools; permissions, steps and results remain visible.", content)

    def es_input(self):
        content = """<div class='grid two'><div class='card'><form method='post'><label>Student ID</label><input name='id' value='SV002'><label>Full name</label><input name='name' value='Trần Bình'><button>Append StudentAdded event</button></form></div>
        <div class='card'><span class='tag'>Event Store</span><h3>Append-only command flow</h3><div class='flow'><span class='node'>Command</span><span class='arrow'>→</span><span class='node'>Event Store</span><span class='arrow'>→</span><span class='node'>Projector</span></div><p>Existing events: <b>%s</b></p></div></div>""" % len(EVENTS)
        return layout("Event Sourcing — input", "A command appends an immutable event; a projector rebuilds the read model.", content)

    def es_list(self):
        rows = [[x["id"], x["name"], x["score"] if x["score"] is not None else "—"] for x in project()]
        return layout("Event Sourcing — student list", "Query reads the projected Read Model, not the Event Store.", table(["Student ID", "Name", "Architecture score"], rows))

    def eda_input(self):
        last = PROCESSED[-1] if PROCESSED else {"eventId": "demo-001", "type": "ReservationCreated", "consumer": "notification-service", "status": "processed"}
        content = f"""<div class='grid two'><div class='card'><form method='post'><label>Hotel ID</label><input name='hotelId' value='hotel-01'><button>Publish ReservationCreated</button></form></div>
        <div class='card'><span class='tag'>Latest event</span><h3>{last['type']}</h3><p>eventId: <b>{last['eventId']}</b></p><p>Consumer: {last['consumer']}</p><p class='ok'>Status: {last['status']}</p></div></div>
        <div class='flow'><span class='node'>Producer</span><span class='arrow'>event →</span><span class='node'>Broker</span><span class='arrow'>event →</span><span class='node'>Consumer</span></div>"""
        return layout("Event-Driven — publish input", "Producer validates input, emits an event, and an independent consumer processes it.", content)

    def kappa_input(self):
        content = """<div class='grid two'><div class='card'><form method='post'><label>Category</label><select name='category'><option>Hotel</option><option>Flight</option></select><label>Amount</label><input name='amount' type='number' value='150'><button>Append event to stream</button></form></div>
        <div class='card'><span class='tag'>Kafka log</span><h3>Single stream pipeline</h3><div class='flow'><span class='node'>Input</span><span class='arrow'>→</span><span class='node'>Log</span><span class='arrow'>→</span><span class='node'>Aggregate</span></div><p>Raw events retained: <b>%s</b></p></div></div>""" % len(RAW_EVENTS)
        return layout("Kappa — event input", "New data enters the same durable stream used for replay.", content)

    def kappa_report(self):
        rows = [[x["category"], x["count"], f"${x['sum']}"] for x in aggregate()]
        cards = "<div class='grid'>" + "".join(f"<div class='card'><span class='tag'>{x['category']}</span><div class='metric'>${x['sum']}</div><p>{x['count']} events</p></div>" for x in aggregate()) + "</div>"
        return layout("Kappa — near-real-time report", "Stream processor deduplicates and aggregates; Report API reads the Serving DB.", cards + "<br>" + table(["Category", "Count", "Total"], rows))

    def kappa_raw(self):
        rows = [[x["eventId"], x["time"], x["category"], x["amount"]] for x in RAW_EVENTS]
        return layout("Kappa — raw report data", "These retained events produce the aggregate report.", table(["Event ID", "Time", "Category", "Amount"], rows))

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8090), Handler)
    print("Demo running at http://localhost:8090")
    server.serve_forever()

