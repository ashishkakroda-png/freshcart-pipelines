# Part D — ACK/NACK viva answers

- With manual acknowledgements, if a driver crashes before sending ACK, RabbitMQ can redeliver the unacknowledged message after the consumer/channel/connection closes. This is at-least-once delivery, so consumers should be idempotent.
- `basic_nack(requeue=False)` rejects and discards the message unless a dead-letter exchange is configured. The exercise uses this for a message missing `zone`.
- If a permanently bad message is NACKed with `requeue=True`, it can be delivered repeatedly, creating a poison-message loop and consuming broker/consumer resources.
- A valid message is ACKed only after the driver has processed it. A malformed JSON message is also rejected without requeue in the supplied driver.
