# SQL and data engineering standards

Apply these rules to SQL, batch processing, streaming jobs, data models and analytical pipelines. Also follow the language profile for the implementation language and the applicable [data engineering defensive patterns](../defensive-patterns/data-engineering.md).

## Data contracts and grain

State the business meaning, row grain, primary key, uniqueness assumptions, null semantics, units, timezone and update cadence of every important dataset. Distinguish event time, processing time and business date. Do not join datasets until their grain and key cardinality are understood.

## SQL design

- Name columns explicitly; avoid SELECT * in production models and interfaces.
- Make join keys and expected one-to-one, one-to-many or many-to-many cardinality explicit.
- Handle duplicate keys, nulls and late-arriving data deliberately.
- Apply partition filters and predicate pushdown where supported; verify the actual query plan for expensive jobs.
- Use deterministic deduplication with a documented tie-break rule.
- Make incremental logic idempotent and define backfill and reprocessing behavior.
- Avoid hiding business logic in deeply nested expressions or repeated copies of the same calculation.
- Document metric definitions, aggregation grain and numerator/denominator semantics.

## Batch engines and warehouses

For Hive, Spark SQL, MaxCompute and similar engines, validate partition pruning, shuffle volume, skew, join strategy, data-size assumptions and scan cost. Prefer engine-supported functions and syntax; do not assume dialects are interchangeable. Test boundary dates, empty partitions, late data and reruns.

## Streaming systems

For Flink, Kafka and similar systems, define event-time and watermark behavior, ordering assumptions, state size and TTL, checkpoint/restart behavior, delivery guarantees and sink commit semantics. Monitor source lag, backpressure, checkpoint duration, restart loops and sink throughput. Do not claim exactly-once end-to-end unless every source, transformation and sink boundary supports the guarantee.

## dbt and modeled datasets

Keep source declarations, model dependencies, tests, documentation and materialization strategy aligned. Test uniqueness, not-null, relationships and accepted values where they express real contracts. Make incremental predicates and unique keys explicit. Review compiled SQL and execution plans for critical models.

## Data quality and operations

Test freshness, completeness, uniqueness, validity, reconciliation and distribution changes according to business risk. Alert on actionable conditions and include affected partition, dataset and safe remediation guidance. Keep secrets and sensitive row-level data out of logs and test fixtures.

## Database changes

Review indexes, constraints, locks, transaction boundaries, online migration support and rollback or forward-recovery behavior. Test migrations against representative data volume and supported database versions.
