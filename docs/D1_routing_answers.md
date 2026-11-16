# Part D1 — Topic routing answers

RabbitMQ topic patterns: `*` matches exactly one dot-separated word; `#` matches zero or more words.

| # | Routing key | Receiving queues |
|---:|---|---|
| 1 | `bangalore.koramangala.food` | Ravi (`bangalore.koramangala.*`), Meena (`bangalore.*.food`), Control (`bangalore.#`) |
| 2 | `bangalore.indiranagar.ride` | Priya (`bangalore.indiranagar.*`), Arjun (`bangalore.*.ride`), Control (`bangalore.#`) |
| 3 | `bangalore.whitefield.ride` | Arjun (`bangalore.*.ride`), Control (`bangalore.#`) |
| 4 | `chennai.tnagar.food` | Karthik (`chennai.tnagar.food`) |
| 5 | `chennai.whitefield.ride` | dropped (no binding matches) |
| 6 | `bangalore.koramangala` | Control only (`bangalore.#`) |

For key 6, the key has two words. All specific three-word bindings require three words and therefore do not match. The `#` wildcard can match zero or more words after `bangalore`, so `bangalore.#` matches the remaining single word `koramangala`.
