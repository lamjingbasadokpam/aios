# AIOS Runtime Tracing V0

Phase 47 projects runtime events into an execution trace.

```text
Runtime Events
      |
      v
TraceBuilder
      |
      v
ExecutionTrace
      |
      +--> spans
      +--> timing
      +--> status
      +--> attributes
```

## Scope

V0 is an in-memory projection layer. It reconstructs spans from correlated `*.started`/`*.called` and `*.completed`/`*.failed` events. It does not collect metrics, export OpenTelemetry, or prescribe a UI.

## Design rules

- Correlation IDs scope a trace projection to one execution.
- Span IDs come from event payloads when available, otherwise the event ID is used.
- Trace construction is read-only and has no execution side effects.
- The event store remains the source of runtime history; traces are derived views.
- Provider-specific telemetry integrations can be added later without changing runtime event contracts.
