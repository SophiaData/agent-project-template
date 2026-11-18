# Documentation instructions

These instructions apply to every file under docs/. Read docs/documentation.md for the full documentation standard and use the document's owning tier for each fact.

- Keep documentation aligned with current shipped behavior. Put historical rationale in decision records or postmortems, not in current-state references.
- Give each fact one authoritative home. Link to the owner instead of copying API details, package inventories, command lists or lower-level procedures.
- Architecture documents describe system context, boundaries, ownership and data flow. Module references describe their own contracts. Decision records explain durable rationale. Upgrade guides describe exact user migration steps.
- Keep tutorials sequential and references organized for lookup. Do not mix a long tutorial and exhaustive reference into one undifferentiated page.
- Preserve ownership, failure behavior, timing, units, defaults, security and compatibility details when editing prose or examples.
- Defensive patterns must describe a concrete trigger, required invariant, failure prevented, observable evidence, boundary/exception and contrasting incorrect/correct examples. Keep applicability narrow; do not turn a local defect into a universal rule.
- Verify relative links, commands, code examples and generated references. Never claim an example or check was executed unless it was.
- Update the owning document in the same change as the code, API, configuration or data contract it describes.
