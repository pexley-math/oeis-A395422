# Design Rationale -- fixed-polyiamond-container

## Chosen approach

Subclass `sat_utils.frameworks.ContainerSolverFramework` with a
triangular-lattice parity-dependent `_neighbors_for_geometry` override.
Everything else (SAT + CEGAR connectivity via CaDiCaL, top-down
minimum-k search, versioned JSON output, CLI wrapper, solver banner)
comes from the shared library. The entire project-side solver is ~100
lines of glue: one subclass (~20 lines), one dataclass instance (~40
lines), and a banner helper that sanity-checks the A001420 fixed
polyiamond counts. Matches Proposal 1 in `research/creative-review.md`.

## Why this approach won the decision tree

1. **Proved on 3 analog projects.** `ContainerSolverFramework` already
   backs oeis-a000217x (hex, fixed polyhexes), oeis-a392363 (triangular,
   free polyiamonds), and the shell family via Phase 9 migration. All
   are DRAFT READY or SUBMITTED.
2. **Triangular neighbours + parity placement are the only novel bits.**
   The shared library provides both: `placement_runner` auto-enables
   `parity_preserving=True` for `geometry="triangular"`, and the
   subclass hook for `_neighbors_for_geometry` covers the CEGAR
   connectivity side.
3. **No shape pruning.** `use_shape_pruning=False` is the framework
   default; the 2026-04-11 bisect retired that heuristic for all
   triangular container variants after the polyiamond-container
   correctness fix. This project MUST NOT re-enable it.
4. **Cross-project reuse beats one-off solvers.** The archived
   2026-03-22 solver was already a framework subclass -- our rewrite
   is almost identical in structure and matches the cookbook pattern
   for "container + triangular + fixed".

## Alternatives considered (and rejected)

- **Proposal 2: top-down search with CEGAR containment verifier.**
  Rejected as the primary solver. Higher runtime risk under the new
  30-minute per-term budget (`SOLVER_ITERATE_TIMEOUT_S=1800`). Retained
  as the second independent verifier in `/solver-verify` where its
  different code path buys us mathematical diversity.
- **Proposal 3: reuse the sibling oeis-new-polyiamond-container
  solver.** Rejected because that project solves the FREE polyiamond
  variant. Converting it in place would couple us to that sibling's
  bug surface (recall the use_shape heuristic bit both).
- **A fresh hand-rolled CP-SAT solver.** Rejected on shared-lib-first
  grounds: `feedback-shared-library-first.md` says reusable code
  belongs in shared libs, not project code. Writing a one-off would
  duplicate ~500 LOC and re-introduce the same latent bug classes the
  framework already guards against.

## Expected performance characteristics

- a(1..9) all solve in well under 1 second each on a cold run (the
  archived use_shape buggy solver was orders of magnitude slower; our
  new solver does it with the framework's C-accelerated placement
  enumerator + CaDiCaL in what should be comparable or faster time).
- Benchmark set (under `BENCHMARK_TIMEOUT_S=120s` per term) is
  expected to reach n >= 10, possibly n = 15 or higher. The
  `BENCHMARK_MAX_N=20` hard cap will likely fire before any term
  exceeds 2 minutes.
- Under the new `SOLVER_ITERATE_TIMEOUT_S=1800s` (30 min) cap,
  `/solver-iterate` is expected to push to n = 12-14. Beyond that the
  (fixed) polyiamond count explodes (A001420 grows ~3.6^n), and SAT
  encoding size grows with it.

## Sanity checks already run

- Smoke test n=1..6 on the new solver: a(1..6) = 1, 4, 6, 9, 12, 17.
  All terms proved, total elapsed < 1 s.
- A001420 count sanity check (n=1..10): all counts match the tabled
  reference values, verifying the polyform_enum Cython backend is
  returning the right fixed-polyiamond sets.

## Known caveats / divergence from the 2026-03-22 run

- The 2026-03-22 archive reported a(1..10) = 1, 3, 5, 8, 11, 15, 19,
  24, 29, 35 (a provisional match with A024206 shifted by +1). That
  run used a placement enumeration that did NOT respect the
  triangular-lattice parity guard, so it over-counted placements by
  treating odd-parity (dr+dc) translations as rigid motions. The new
  run's values differ from n=2 onward (a(2) = 4, not 3), which breaks
  the A024206 match at the very first non-trivial term.
- The prior-art-search verdict (`FOUND (extending A024206)`) was
  recorded on the stale premise. It will need to be reconciled with
  the re-run values in `/conjecture-search` and `/paper-draft`.
- The `use_shape_pruning=False` rule is enforced by the framework
  default; the project solver never sets it to True. Any downstream
  "optimisation" that re-enables it is forbidden per
  `feedback-heuristic-ablation-mandatory.md`.
