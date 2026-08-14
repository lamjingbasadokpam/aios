# AIOS Runtime Budgets V0

Phase 51 adds quantitative resource governance to the runtime.

## Budget dimensions

- maximum model tokens
- maximum runtime seconds
- maximum tool calls
- maximum retries
- maximum estimated cost

```text
Run
 |
 +--> Policy / capability checks
 |
 +--> BudgetPolicy
 |       |
 |       +--> tokens
 |       +--> time
 |       +--> tools
 |       +--> retries
 |       +--> cost
 |
 +--> ALLOW / DENY
```

## Rules

- Limits are optional; unspecified resources are not constrained by this policy.
- Evaluation is deterministic and fail-closed when a configured limit is exceeded.
- Budget policy observes usage; it does not calculate missing token or cost data.
- Enforcement/admission integration belongs to the execution runtime.
- A future accounting layer can accumulate usage from runtime events without coupling the budget model to a specific provider.
