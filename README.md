# OEIS -- fixed-polyiamond-container

Solver code, data, paper, and figures for the **minimum-size connected
polyiamond that contains every fixed n-iamond as a translated subset**
on the triangular lattice.

## Problem

For n >= 1, let a(n) be the minimum number of triangular cells in a
connected polyiamond C such that every fixed n-iamond P is a subset of
C after some parity-preserving translation. A fixed n-iamond is a
connected set of n unit triangles considered up to translation only;
rotations and reflections yield distinct pieces, so |F(n)| matches
OEIS A001420 (2, 3, 6, 14, 36, 94, 250, 675, 1838 for
n = 1..9 -- note A001420(1) = 2, not 1, because the triangular
lattice has two distinct unit-triangle orientations).

Grid: **triangular** (parity-dependent 3-neighbour adjacency).
Problem family: **container**.

## Proved values (n = 1..9, unconditional)

```
a(1..9) = 2, 4, 6, 9, 12, 17, 22, 27, 31
```

Every value is proved by the main SAT solver (CaDiCaL 1.5.3 + CEGAR
connectivity + ITotalizer incremental descent) inside the n x n window
AND re-verified inside the strictly larger (n+1) x (n+1) window with a
drat-trim VERIFIED DRAT proof (verdict `s DERIVATION`) of UNSAT at
size a(n) - 1. The wider-window step rules out the only structural
assumption the n x n search could leave open, making each reported
value unconditional within the (n+1) x (n+1) window.

Each value is additionally cross-verified by two further verifiers
with disjoint code paths:
- **Verifier 1** -- pure-Python geometric containment verifier.
- **Verifier 2** -- Glucose 4.2 with a rooted spanning-arborescence
  connectivity encoding and a sequential-counter cardinality encoding.

See `submission/paper.md` for the full computational-methodology
description and the per-n SAT witnesses.

## Key results

- **Theorem 1 (unconditional).** a(n) = 2, 4, 6, 9, 12, 17, 22, 27, 31
  for n = 1..9, proved via (SAT witness, drat-trim VERIFIED DRAT UNSAT
  at k - 1) pairs in the wider (n+1) x (n+1) search window.
- **Open Problem 1 (unrestricted Assumption (S)).** Whether some
  minimum container for F(n) fits in any bounded rectangle as n grows
  remains open in general. The wider-window step settles it for
  n = 1..9 within the (n+1) x (n+1) window. Four classical structural
  attacks (MCS pairwise overlap, Barequet-Ben Shachar 2022 inflation,
  LP duality, local exchange / notch shift) are documented in
  `../open-problem-A395422/literature-alternatives.md` as inapplicable
  or insufficient for the Theta(n^2) growth regime.
- **A024206 conjecture falsified.** The 2026-03-22 prior-art pass
  noted a match with a shift of A024206; the corrected solver
  values no longer match A024206 under any shift.
- **No closed form found.** Seven candidate formulas across five
  categories all fail.
- **Cap structure conjecture.** Caps appear at n = 1 mod 4 (n=5 saves
  1 cell, n=9 saves 2 cells); predicts n=13 saves 3 cells.
- **n = 10 (a = 39) parked.** Solver-verified at 39 cells, but still
  conditional on Assumption (S); excluded from the n=1..9 publication
  scope. Wider-window verification at n=10 in 11x11 is estimated at
  ~20 minutes; n=11 reachable on dedicated compute (~48-hour budget).

## Status

**DRAFT READY (n = 1..9 unconditional, revised 2026-04-20).** Paper,
Typst, OEIS draft, HTML helper, and figures all updated. Pipeline
skills 1-11 complete; skill 12 (project-validate) is the final
automated gate.

Paper PDF at `submission/paper.pdf`.
Publication and personal-understanding figures at
`submission/fixed-polyiamond-container-figures.pdf` and
`research/fixed-polyiamond-container-understanding.pdf`.

The OEIS submission draft (new sequence) is prepared at
`submission/oeis-draft.txt`, with a click-to-copy helper at
`submission/oeis-copy-helper.html`.

## Files

- `code/solve_fixed-polyiamond-container.py` -- main solver
- `code/verify_method1.py` -- independent pure-Python containment
  verifier
- `code/verify_method2.py` -- independent Glucose-based re-optimiser
- `research/solver-results.json` -- proved values, witnesses, timings
- `research/verify_method{1,2}-results.json` -- verifier results
- `research/conjecture-report.md` -- conjecture-search output
- `research/verification-report.md` -- solver-verify skill output
- `research/design-rationale.md` -- solver-design skill output
- `submission/paper.md` -- polished Markdown (222 lines)
- `submission/paper.typ` -- Typst source
- `submission/paper.pdf` -- compiled PDF
- `submission/fixed-polyiamond-container-figures.pdf` -- publication figures
- `submission/oeis-draft.txt` -- OEIS submission draft (new sequence)
- `submission/oeis-copy-helper.html` -- click-to-copy helper for the OEIS web form
- `research/fixed-polyiamond-container-understanding.pdf` -- personal-understanding diagram

## License

CC-BY-4.0. See `LICENSE`.
