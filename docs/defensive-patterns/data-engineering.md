# Data engineering defensive patterns

Apply these patterns to SQL models, warehouse tables, batch pipelines, streaming jobs, event contracts and analytical datasets. They supplement [SQL and data engineering standards](../standards/data-engineering.md).

## Declare data grain before joining or aggregating

### Applies when
A model, query or pipeline combines datasets, changes aggregation level or publishes a reusable fact or dimension.

### Required invariant
State what one row represents, the key at that grain, and the intended output grain before writing joins or aggregates. Every aggregation must preserve or deliberately change that grain.

### Failure prevented
Fan-out joins, accidental double counting, ambiguous metrics and facts that cannot be reconciled to their source records.

### Evidence
Document the row grain and key in the model contract. Test uniqueness at the declared grain and reconcile representative totals before and after joins or aggregation.

### Boundary and exception
A raw event table may intentionally preserve duplicate deliveries or lack a business key. Document that raw grain explicitly; do not silently treat it as a deduplicated fact.

### Incorrect example
~~~sql
SELECT product_id, SUM(spend) AS spend
FROM ad_cost a
JOIN product_sale s
  ON a.product_id = s.product_id
GROUP BY product_id;
~~~

### Correct example
~~~sql
-- First define the output grain and aggregate each input to that grain.
WITH cost_by_product AS (
    SELECT product_id, SUM(spend) AS spend
    FROM ad_cost
    GROUP BY product_id
),
sale_by_product AS (
    SELECT product_id, COUNT(DISTINCT sale_id) AS sale_count
    FROM product_sale
    GROUP BY product_id
)
SELECT c.product_id, c.spend, s.sale_count
FROM cost_by_product c
LEFT JOIN sale_by_product s
  ON c.product_id = s.product_id;
~~~

### Enforcement
Model review and automated uniqueness/reconciliation tests where the engine and data volume permit them.

## Verify join cardinality instead of assuming it

### Applies when
A join expects one-to-one or many-to-one behavior, or when either side may contain duplicate keys.

### Required invariant
Prove the expected key cardinality on both sides or handle duplicates with a deterministic business rule before relying on the join.

### Failure prevented
Unexpected row multiplication, dropped records, unstable deduplication and inflated spend, order or conversion metrics.

### Evidence
Run duplicate-key checks on the relevant partition or representative sample. Compare row counts and business totals before and after the join. Include null-key behavior in the contract.

### Boundary and exception
Many-to-many joins are valid when the relationship itself is many-to-many and the output grain accounts for it. The rule is to model the multiplication explicitly, not to prohibit it.

### Incorrect example
~~~sql
-- Assumes product_id is unique in product_info without checking.
SELECT f.product_id, f.spend, d.category
FROM fact_spend f
LEFT JOIN product_info d
  ON f.product_id = d.product_id;
~~~

### Correct example
~~~sql
SELECT product_id, COUNT(*) AS row_count
FROM product_info
GROUP BY product_id
HAVING COUNT(*) > 1;
~~~

Resolve the reported duplicates with an explicit effective-date, priority or other domain tie-break before using the dimension as many-to-one.

### Enforcement
SQL tests or pre-aggregation checks plus review of the documented cardinality.

## Keep event time, processing time and business date distinct

### Applies when
A pipeline uses timestamps, time zones, event windows, daily partitions, late data or business-calendar reporting.

### Required invariant
Name the clock used by each filter, window and partition. Convert time zones explicitly and define the rule that maps an event timestamp to a business date.

### Failure prevented
Missing or duplicated boundary events, incorrect daily totals, daylight-saving errors and inconsistent reports between source and warehouse.

### Evidence
Test events around midnight, partition boundaries, daylight-saving transitions where applicable, late arrivals and replay. Record the source timezone and target business timezone.

### Boundary and exception
A source that guarantees UTC timestamps may use UTC as its source contract. Do not infer a business date from ingestion time unless ingestion time is the explicitly chosen business rule.

### Incorrect example
~~~sql
WHERE event_time >= business_day_start
  AND event_time < next_business_day_start
~~~

### Correct example
~~~sql
-- Convert the source instant to the reporting timezone, then apply a
-- half-open local business-date interval using engine-supported functions.
WHERE local_event_time >= business_day_start
  AND local_event_time < next_business_day_start
~~~

### Enforcement
Boundary fixtures and reconciliation tests; review timezone and partition semantics together.

## Incremental processing is idempotent and replayable

### Applies when
A job reads a moving time or partition window, performs upserts, consumes events, backfills history or retries after failure.

### Required invariant
Define the input interval, overlap policy, deduplication key, write semantics and replay behavior. Reprocessing the same logical input must not create unintended duplicate effects.

### Failure prevented
Gaps between windows, duplicate facts after retries, inconsistent backfills and late data that can never be corrected.

### Evidence
Run the same input twice and compare output state. Test adjacent window boundaries, late-arriving records, partial failure and backfill. Verify that overwrite or merge scope is limited to the intended data.

### Boundary and exception
Append-only raw landing may intentionally retain every delivery. Its delivery identity and downstream deduplication contract must still be explicit.

### Incorrect example
~~~text
Read only records newer than the last observed maximum timestamp,
then append every row without a stable event key.
~~~

### Correct example
~~~text
Read a documented half-open interval with an overlap where required,
deduplicate by a stable source key and deterministic version, then
merge or overwrite the owned output partitions idempotently.
~~~

### Enforcement
Replay and duplicate-input tests plus review of the source offset, watermark or partition-window contract.

## Treat delivery guarantees as end-to-end contracts

### Applies when
A system claims at-most-once, at-least-once, exactly-once, transactional or effectively-once processing across sources, transformations and sinks.

### Required invariant
State the guarantee at each boundary and the failure cases it covers. Do not describe an end-to-end pipeline as exactly-once when one connector, external side effect or sink commit boundary permits duplicates or loss.

### Failure prevented
False reliability guarantees, duplicate external effects after recovery and data loss hidden by checkpoint success.

### Evidence
Exercise failure before and after checkpoint, transaction prepare/commit, sink acknowledgement and restart. Reconcile source progress with durable sink state.

### Boundary and exception
A connector's documented guarantee may be stated for that connector alone. Label its scope and do not extend it to external systems that are outside the transaction.

### Incorrect example
~~~text
The job uses checkpoints, therefore the entire business workflow is exactly-once.
~~~

### Correct example
~~~text
Source offsets and the transactional table sink recover consistently
through checkpointed commits. The downstream HTTP notification is
at-least-once and uses an idempotency key to contain duplicates.
~~~

### Enforcement
Integration or recovery tests against the real connector path where feasible; explicit review of every source, state and sink boundary.

## Evolve schemas without silently changing meaning

### Applies when
A pipeline changes table columns, event fields, serialized payloads, partition layouts, keys or persisted formats.

### Required invariant
Define reader and writer compatibility, null/default behavior, historical data handling and migration order. A field must not be reused for a different meaning without a versioned migration.

### Failure prevented
Old consumers failing on new data, historical partitions becoming unreadable, silent metric reinterpretation and mixed-version deployments producing incompatible records.

### Evidence
Test old and new representative records against supported readers. Validate backfill, mixed-version operation and rollback or forward recovery. Compare schema metadata as well as sample values.

### Boundary and exception
An ephemeral internal dataset may have a shorter compatibility window when all consumers and retained data are known and migrated together. Record that scope and owner explicitly.

### Incorrect example
~~~text
Rename a persisted field in place and assume all historical partitions
and downstream readers will use the new name.
~~~

### Correct example
~~~text
Add the new field with defined null/default semantics, update readers
to support both forms, backfill and reconcile historical data, then
retire the old field only after supported consumers have migrated.
~~~

### Enforcement
Schema/contract tests, migration validation and compatibility review.
