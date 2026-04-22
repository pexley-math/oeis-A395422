# OEIS A395422 -- Smallest Connected Polyiamond Containing All Fixed n-Iamonds

Solver code and data for [OEIS A395422](https://oeis.org/A395422).

## The Problem

a(n) is the minimum number of triangular cells in a connected polyiamond C such that every fixed n-iamond P is a subset of C after some parity-preserving translation of the triangular lattice. A fixed n-iamond is a connected set of n unit triangles counted up to translation only; rotations and reflections yield distinct pieces, so the number of fixed n-iamonds is [A001420(n)](https://oeis.org/A001420) (2, 3, 6, 14, 36, 94, 250, 675, 1838 for n = 1..9 -- note A001420(1) = 2, since the triangular lattice has two distinct unit-triangle orientations). This is the triangular-grid fixed-piece analog of [A327094](https://oeis.org/A327094) (square grid, free pieces) and the triangular-grid counterpart of [A392363](https://oeis.org/A392363) (triangular grid, free pieces).

## Results

**New proved terms (this work):**

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **a(n)** | **2** | **4** | **6** | **9** | **12** | **17** | **22** | **27** | **31** |
| **Pieces (A001420)** | 2 | 3 | 6 | 14 | 36 | 94 | 250 | 675 | 1838 |
| **Main bbox** | 1x2 | 2x2 | 2x3 | 3x4 | 4x5 | 4x6 | 4x7 | 5x8 | 6x9 |
| **Main time (s)** | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.016 | 0.079 | 0.840 | 4.911 |
| **Wider-window time (s)** | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.2 | 0.6 | 9.0 | 58.7 |

Each value is proved by matching SAT/UNSAT certificates (SAT at k = a(n), UNSAT at k = a(n) - 1) inside an n x n search rectangle, then re-verified in a strictly larger (n+1) x (n+1) window with a drat-trim VERIFIED DRAT proof of UNSAT (verdict `s DERIVATION`). Every container is additionally cross-checked by two further verifiers with disjoint code paths: a pure-Python geometric containment verifier and an independent Glucose-based re-optimiser with a rooted spanning-arborescence encoding.

## Method

SAT solver (CaDiCaL 1.5.3 via PySAT) with counterexample-guided abstraction refinement (CEGAR) for connectivity and top-down incremental descent via an ITotalizer wrapper.

- **SAT encoding:** cell variables x(r, c) with an exact-k cardinality constraint (totalizer), placement variables y(i, t) for each fixed n-iamond P_i and each parity-preserving lattice translation t that fits inside the search rectangle, plus piece-coverage and piece-cell implication clauses.
- **Connectivity:** enforced via CEGAR -- each candidate model is BFS-tested under the parity-dependent 3-neighbour adjacency; disconnected models trigger a disjunctive cut and a re-solve until the returned cell set is a single connected component.
- **Wider-window verification:** the lower-bound instance at k = a(n) - 1 is re-solved inside the (n+1) x (n+1) window with an explicit translation-symmetry breaker, emitting a DRAT proof that is independently checked by drat-trim. This closes the only structural loophole the n x n search could leave open.
- **No shape-constraint heuristics:** a 2026-04-11 bisect showed that row-contiguity / canonical-bbox pruning silently dropped pieces on the triangular lattice; the solver uses no such heuristic and depends only on the A001420 piece count (checked at startup), parity-preserving placement enumeration, and CEGAR connectivity.

## Key Findings

- The sequence is novel: no match against any shift of [A024206](https://oeis.org/A024206), no polynomial fit (non-constant second differences), no Berlekamp-Massey linear recurrence of order <= 5.
- Growth appears to be Theta(n^2) with a(n) / n^2 drifting from 2.000 at n = 1 down to 0.383 at n = 9.
- **Cap-row structure.** At n = 5 and n = 9 the optimal container has row span one greater than the maximum row span of any single n-iamond; an isolated "cap" cell in the extra row is load-bearing (removing it forces an extra cell elsewhere). Both indices satisfy n = 1 (mod 4); the pattern is conjectural but predicts a 3-cell cap saving at n = 13 if it persists.
- **No closed form found.** Seven candidate formulas across five categories (general polynomial, quadratic, triangular numbers, density heuristic, linear recurrence, A024206 shifts, power-law asymptotic) all fail.

## Running the Solver

**Requirements:** Python 3.12+, python-sat (PySAT with CaDiCaL 1.5.3 and Glucose 4.2). The wider-window and prose-trace pipelines additionally need drat-trim (MSVC build for Windows, standard `make` for Linux) and native cadical 3.0.0.

```bash
# Main solver -- proves a(n) inside the n x n search rectangle
python code/solve_fixed-polyiamond-container.py --n 1-9 --per-term-timeout 1800

# Independent verifier 1 -- pure-Python geometric containment
python code/verify_method1.py 9

# Independent verifier 2 -- Glucose + rooted spanning arborescence, re-derives a(n)
python code/verify_method2.py 9 --per-term-timeout 7200
```

## Files

| File | Description |
|------|-------------|
| `code/solve_fixed-polyiamond-container.py` | SAT solver with CEGAR connectivity and ITotalizer descent |
| `code/verify_method1.py` | Independent verifier (pure-Python geometric containment) |
| `code/verify_method2.py` | Independent verifier (Glucose + spanning-arborescence re-optimiser) |
| `code/extract_proof.py` | Prose trace + MUC + implication DAG renderer |
| `code/generate-figures.py` | Publication figure generator |
| `research/solver-results.json` | Machine-readable results with witnesses and timings |
| `research/solver-run-log.txt` | Solver run log |
| `research/verify_method{1,2}-results.json` | Per-term verifier results |
| `research/drat/` | CNF, DRAT, witness, and sidecar artefacts for each n |
| `research/drat-certification-summary.json` | Per-n drat-trim verdicts |
| `research/proof-trace.md` | Prose trace + MUC statistics for n = 1..5 |
| `submission/paper.pdf` | Research paper |
| `submission/fixed-polyiamond-container-figures.pdf` | Publication figures |
| `submission/oeis-draft.txt` | OEIS submission draft |

## Prior Art and Acknowledgments

This is a new sequence -- no prior OEIS entry exists for this problem. The square-grid free-piece analog is [A327094](https://oeis.org/A327094), submitted to OEIS by Peter Kagey (Sep 2019); the underlying Minimum Common Superform question for pentominoes was posed by T. R. Dawson in 1942 (*Fairy Chess Review* Vol. 5 No. 4). The triangular-grid free-piece analog is [A392363](https://oeis.org/A392363); the hexagonal-grid fixed-piece analog matches the triangular numbers [A000217](https://oeis.org/A000217) for n = 1..7. Methodologically this work follows the SAT-based computational-combinatorics tradition exemplified by Heule and Kullmann's Boolean Pythagorean triples proof (2016) and by the DRAT-proof infrastructure developed for SAT Competition instances.

This work was inspired by the [OEIS](https://oeis.org/) and the community of contributors who maintain it.

## Hardware

AMD Ryzen 5 5600 (6-core / 12-thread), 16 GB RAM, Windows 11, single-threaded.

## License

[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) -- Peter Exley, 2026.

This work is freely available. If you find it useful, a citation or acknowledgment is appreciated but not required.

## Links

- **A395422** (this sequence): https://oeis.org/A395422
- **A001420** (fixed n-iamond count, solver input): https://oeis.org/A001420
- **A392363** (triangular grid, free pieces -- companion): https://oeis.org/A392363
- **A327094** (square grid, free pieces): https://oeis.org/A327094
- **A000217** (triangular numbers; hex-grid fixed-piece analog, proved for n = 1..7): https://oeis.org/A000217
- **A024206** (previously conjectured match, falsified in this work): https://oeis.org/A024206
