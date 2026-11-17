---
name: project-simplification
description: Use to identify evidence-backed reductions in code, APIs, configuration, dependencies, state machines, tests or documentation without losing required behavior.
---

# Simplification workflow

1. Establish the user-visible behavior and constraints that must remain.
2. Trace real producers, consumers, public interfaces, configuration, generated outputs and deployment paths.
3. Identify duplicated or unreachable behavior and the maintenance obligations it creates.
4. Compare removal with the smallest alternative; include dependencies, glue, tests and operational cost.
5. State capability or compatibility losses explicitly. Do not call a relocation of complexity a simplification.
6. Prefer a small number of evidence-backed changes over deletion counts or speculative cleanup.
7. Add regression tests for retained behavior and update decision records when the tradeoff is durable.
