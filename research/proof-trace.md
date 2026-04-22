## Container-proof trace: fixed-polyiamond-container n=5

Triangular-grid container problem on a 5 x 5 window; proves a(5) > 11.  Derivation rests on 25 cell variables plus piece-placement auxiliaries; the CNF is UNSAT (refuted by CDCL; DRAT separately).

- Step 1: from clause (1 literals), force NOT cardinality counter (exactly 11 cells, aux var 238).
- Step 2: from clause (1 literals), force NOT cardinality counter (exactly 11 cells, aux var 353).
- Step 3: from clause (2 literals), force NOT cardinality counter (exactly 11 cells, aux var 391).
- Step 4: from clause (2 literals), force NOT cardinality counter (exactly 11 cells, aux var 378).

## Encoding summary

- n = 5 (target: smallest polyiamond containing every fixed n-iamond by translation)
- target lower bound: a(5) > 11  (i.e., no 11-cell polyiamond covers every fixed n-iamond)
- SAT variables: 459
- total clauses: 1883
- renderer template: ``ContainerTemplate`` with descriptor_from_context (shared library, no framework retrofit required)

### Unit-propagation trace stats

- is_unsat_by_up: False
- propagation steps recorded: 4
- conflict: no

### MUC extraction

- drat-trim verdict: REFUTATION
- core clauses: 1274 of 1883
- core fraction: 67.7%

_Note: rendering uses the shared ``sat_utils.prose_trace_container.ContainerTemplate``, constructed from a ``ContainerDescriptor`` derived from the project's own framework instance via ``descriptor_from_context``.  No framework retrofit is required -- cell, piece, symmetry, and CEGAR clauses are recognised from literal shapes.  See ``tools/cadical-support/README.md`` for the native cadical build required by the DRAT emission step._
