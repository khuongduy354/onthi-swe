import json
import logging
import os
import time

from kafka import KafkaConsumer
from opentelemetry.propagate import extract

from telemetry import configure_tracing

logging.basicConfig(level=logging.INFO, format="%(message)s")
tracer = configure_tracing("notification-consumer")


def connect_consumer():
    while True:
        try:
            return KafkaConsumer(
                "reservation-events",
                bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "redpanda:9092"),
                group_id="notification-service",
                auto_offset_reset="earliest",
                value_deserializer=lambda value: json.loads(value.decode()),
            )
        except Exception as exc:
            logging.info(json.dumps({"service": "consumer", "action": "waiting_for_broker", "error": str(exc)}))
            time.sleep(2)


consumer = connect_consumer()
logging.info(json.dumps({"service": "consumer", "action": "ready"}))
for message in consumer:
    headers = {key: value.decode() for key, value in (message.headers or [])}
    parent_context = extract(headers)
    event = message.value
    with tracer.start_as_current_span("notification.handle", context=parent_context) as span:
        span.set_attribute("event.id", event["eventId"])
        span.set_attribute("messaging.destination", message.topic)
        logging.info(json.dumps({
            "service": "consumer",
            "action": "event_processed",
            "partition": message.partition,
            "offset": message.offset,
            **event,
        }))

