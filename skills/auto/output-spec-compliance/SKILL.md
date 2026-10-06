---
name: output-spec-compliance
description: Use when a task states explicit rules about output files, schemas, units, naming, ordering, or required keys, so every mandated property is satisfied before submission.
---
- Before coding, list every stated rule/constraint as a separate, testable obligation.
- Map each obligation to the exact artifact (file, object, key, field) that must satisfy it.
- Convert quantities to the required unit whenever a unit is specified; emit integer minor units when a value is defined in a smaller unit, and keep rounding consistent.
- Apply required identifier normalization (case, separator style) to every affected value, including keys and counts.
- Sort collections by the specified key(s) and direction, adding a deterministic tie-breaker so order is reproducible.
- Include every mandated top-level field or file header (schema/version tags, generator name, source, row counts) with the exact names given.
- Produce every demanded output artifact, including auxiliary files, not just the primary one.
- After generating outputs, programmatically assert each rule (presence of keys, units, sort order, header row) instead of relying on visual inspection.
- Do not declare completion while any enumerated rule remains unverified.
