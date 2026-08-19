import json
import logging
import os
import uuid

import requests
from flask import Flask, jsonify, request
from opentelemetry.propagate import inject

from telemetry import configure_tracing

logging.basicConfig(level=logging.INFO, format="%(message)s")
app = Flask(__name__)
tracer = configure_tracing("gateway-service")
reservation_url = os.getenv("RESERVATION_URL", "http://reservation:8082/reservations")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/availability")
def availability():
    with tracer.start_as_current_span("GET /availability"):
        headers = {}
        inject(headers)
        logging.info(json.dumps({"service": "gateway", "action": "availability_requested", "hotelId": "hotel-01"}))
        response = requests.get(
            os.getenv("RESERVATION_URL", "http://reservation:8082/reservations").replace("/reservations", "/availability"),
            params={"hotelId": "hotel-01"},
            headers=headers,
            timeout=10,
        )
        return jsonify(response.json()), response.status_code


@app.post("/book")
def book():
    body = request.get_json(force=True)
    event_id = str(uuid.uuid4())
    with tracer.start_as_current_span("POST /book") as span:
        span.set_attribute("event.id", event_id)
        headers = {}
        inject(headers)
        logging.info(json.dumps({"service": "gateway", "action": "booking_received", "eventId": event_id}))
        response = requests.post(
            reservation_url,
            json={**body, "eventId": event_id},
            headers=headers,
            timeout=10,
        )
        return jsonify(response.json()), response.status_code


app.run(host="0.0.0.0", port=8081)
