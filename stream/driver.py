"""A driver consumes requests matching its RabbitMQ topic binding.

Usage: python driver.py Ravi 'bangalore.koramangala.*'
Set RABBITMQ_URL for a hosted broker; otherwise localhost guest credentials are used.
"""
from __future__ import annotations
import json
import os
import sys
import pika

EXCHANGE = "rapido-dispatch"


def main(name: str, pattern: str) -> None:
    url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/%2F")
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)
    result = channel.queue_declare(queue="", exclusive=True, auto_delete=True)
    queue = result.method.queue
    channel.queue_bind(exchange=EXCHANGE, queue=queue, routing_key=pattern)
    channel.basic_qos(prefetch_count=1)
    print(f"{name} listening: queue={queue}, binding={pattern}")

    def handle(ch, method, properties, body):
        try:
            message = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            print(f"{name}: malformed JSON; NACK discard ({exc})")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        if not message.get("zone"):
            print(f"{name}: rejected {message.get('id', '<no id>')} - missing zone")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        print(f"{name}: accepted {method.routing_key} -> {message}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=queue, on_message_callback=handle, auto_ack=False)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print(f"{name}: stopping")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python driver.py NAME 'city.zone.type-pattern'")
    main(sys.argv[1], sys.argv[2])
