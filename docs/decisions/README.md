# Engineering decision records

Use a decision record when a choice has durable consequences for architecture, public contracts, data formats, security, reliability, dependencies or engineering policy. Do not create a record for every local implementation detail.

## File and status

Use one dated file per decision: YYYY-MM-DD-short-topic.md. Keep records in this directory and link them from the owning architecture or module documentation.

A record has one status:
- **Proposed:** under review; not yet adopted.
- **Accepted:** adopted and reflected in the implementation.
- **Rejected:** considered and declined; retain only while the rationale prevents a plausible repeated mistake.
- **Superseded:** replaced by a later decision; link the successor and preserve any still-relevant consequences.

## Required content

Copy docs/decisions/template.md. Record the problem, constraints, decision, alternatives, consequences, risks and verification. Be explicit about what was rejected and what capability or flexibility is given up.

Keep accepted records aligned with shipped reality. When a decision changes, create a successor rather than rewriting history into a different decision. Delete or consolidate obsolete records only after preserving unique rationale and repairing inbound links.
