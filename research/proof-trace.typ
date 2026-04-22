== Container-proof trace: fixed-polyiamond-container n=5

Triangular-grid container problem on a 5 x 5 window; proves a(5) > 11.  Derivation rests on 25 cell variables plus piece-placement auxiliaries; the CNF is UNSAT (refuted by CDCL; DRAT separately).

- Step 1: from clause (1 literals), force NOT cardinality counter (exactly 11 cells, aux var 238).
- Step 2: from clause (1 literals), force NOT cardinality counter (exactly 11 cells, aux var 353).
- Step 3: from clause (2 literals), force NOT cardinality counter (exactly 11 cells, aux var 391).
- Step 4: from clause (2 literals), force NOT cardinality counter (exactly 11 cells, aux var 378).
