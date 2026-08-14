# AIOS Runtime Metrics V0

Phase 48 adds provider-neutral metrics derived from runtime events.

## Signals

- event counters by event type
- runtime error count
- model token totals when supplied by the model adapter
- model latency totals when supplied by the model adapter

The metrics layer is intentionally vendor-neutral. Exporters for Prometheus, OpenTelemetry, CloudWatch, or another backend belong in adapters rather than the runtime core.

```text
RuntimeEvent
    |
    v
RuntimeMetrics
    |
    +--> counters
    +--> totals
    +--> gauges (future)
    |
    v
Exporter adapter (future)
```

Metrics are observations, not authorization signals. Missing optional telemetry fields are ignored rather than guessed.
