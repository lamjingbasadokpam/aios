# AIOS Runtime Event Bus V0

Phase 45 introduces a provider-neutral event backbone for the AIOS runtime.

```text
Workflow / Agent / Tool
          |
          v
      RuntimeEvent
          |
          v
       EventBus
       /     \
      v       v
 observers   wildcard subscribers
```

## Event contract

`RuntimeEvent` contains a type, payload, event ID, UTC timestamp, and optional correlation ID.

## V0 implementation

`EventBus` is an in-process asynchronous pub/sub implementation. Subscribers may listen for an exact event type or `*` for all events.

Handler failures are collected and reported after all subscribed handlers have had an opportunity to run. This prevents one observer from silently preventing other observers from receiving an event.

## Design boundary

The event bus is transport-neutral. A future durable or distributed adapter can replace the in-process bus without changing producers' event contracts.

Events are for observation and coordination; they do not grant capabilities or authorization.
