"""Publish food/ride requests to a RabbitMQ topic exchange.

Usage: RABBITMQ_URL=amqp://... python dispatcher.py
Every tenth publication intentionally omits `zone` for the ACK/NACK exercise.
"""
from __future__ import annotations
import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

import pika

EXCHANGE = "rapido-dispatch"
CITIES = {
    "bangalore": ["koramangala", "indiranagar", "whitefield"],
    "chennai": ["tnagar", "velachery", "adyar"],
}
TYPES = ["ride", "food"]


def main() -> None:
    url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    count = 0
    print(f"Publishing to topic exchange {EXCHANGE}; Ctrl+C to stop")
    try:
        while True:
            count += 1
            city = random.choice(list(CITIES))
            zone = random.choice(CITIES[city])
            order_type = random.choice(TYPES)
            routing_key = f"{city}.{zone}.{order_type}"
            message = {
                "id": str(uuid.uuid4()),
                "city": city,
                "type": order_type,
                "ts": datetime.now(timezone.utc).isoformat(),
            }
            # Intentional poison message: valid JSON but missing required `zone`.
            if count % 10 != 0:
                message["zone"] = zone
            body = json.dumps(message).encode("utf-8")
            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(
                    content_type="application/json", delivery_mode=2
                ),
            )
            flag = " BAD(no zone)" if count % 10 == 0 else ""
            print(f"#{count} {routing_key} {message['id']}{flag}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopping dispatcher")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
