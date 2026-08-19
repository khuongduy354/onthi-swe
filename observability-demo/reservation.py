import json
import logging
import os
import time

from flask import Flask, jsonify, request
from kafka import KafkaProducer
from opentelemetry.propagate import extract, inject
from opentelemetry.trace import use_span

from telemetry import configure_tracing

logging.basicConfig(level=logging.INFO, format="%(message)s")
app = Flask(__name__)
tracer = configure_tracing("reservation-service")


def connect_producer():
    while True:
        try:
            return KafkaProducer(
                bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "redpanda:9092"),
                value_serializer=lambda value: json.dumps(value).encode(),
            )
        except Exception as exc:
            logging.info(json.dumps({"service": "reservation", "action": "waiting_for_broker", "error": str(exc)}))
            time.sleep(2)


producer = connect_producer()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/availability")
def availability():
    parent_context = extract({key.lower(): value for key, value in request.headers.items()})
    with tracer.start_as_current_span("availability.check", context=parent_context) as span:
        hotel_id = request.args.get("hotelId", "unknown")
        span.set_attribute("hotel.id", hotel_id)
        logging.info(json.dumps({"service": "reservation", "action": "availability_checked", "hotelId": hotel_id, "available": True}))
        return {"hotelId": hotel_id, "available": True}


@app.post("/reservations")
def create_reservation():
    # W3C propagator expects the lowercase ``traceparent`` key. Flask exposes
    # it as ``Traceparent``, so normalize the carrier before extracting it.
    parent_context = extract({key.lower(): value for key, value in request.headers.items()})
    with tracer.start_as_current_span("reservation.create", context=parent_context) as span:
        body = request.get_json(force=True)
        event_id = body["eventId"]
        span.set_attribute("event.id", event_id)
        carrier = {}
        inject(carrier)
        event = {
            "eventId": event_id,
            "type": "ReservationCreated",
            "hotelId": body.get("hotelId"),
            "userId": body.get("userId"),
        }
        producer.send(
            "reservation-events",
            event,
            headers=[(key, value.encode()) for key, value in carrier.items()],
        ).get(timeout=10)
        logging.info(json.dumps({"service": "reservation", "action": "event_published", **event}))
        return jsonify({"status": "accepted", **event}), 202


app.run(host="0.0.0.0", port=8082)
