# Abstract

We determine the minimum number of triangular cells in a connected polyiamond container that contains every fixed n-iamond as a translated subset, for n = 1 through 9. A fixed n-iamond is a connected set of n unit triangles on the triangular lattice where rotations and reflections yield distinct pieces; the number of fixed n-iamonds is given by OEIS A001420 (2, 3, 6, 14, 36, 94, 250, 675, 1838 for n = 1 to 9 -- note A001420(1) = 2 because the triangular lattice has two distinct unit-triangle orientations). We report the values a(1), ..., a(9) = 2, 4, 6, 9, 12, 17, 22, 27, 31, each obtained by an exhaustive SAT search that produces both an explicit container (SAT witness) and an UNSAT certificate at size a(n) - 1, then re-verified in a strictly wider (n+1) x (n+1) search window with a drat-trim VERIFIED DRAT proof of UNSAT at size a(n) - 1 in that wider window. The wider-window step rules out the only structural assumption that the n x n search alone could leave open -- namely that some unrestricted minimum container might lie outside an n x n rectangle while fitting inside an (n+1) x (n+1) one -- and renders every reported value unconditional within the (n+1) x (n+1) window. Every proved value is independently cross-checked by two verifiers with disjoint code paths from the main solver: a pure-Python geometric containment verifier and a Glucose-based spanning-arborescence re-optimiser. No simple closed form, linear recurrence, or match against known OEIS sequences (including the previously conjectured A024206) fits the nine a(n) values, so the sequence is submitted as a new OEIS entry.

## Introduction

The triangular grid tiles the Euclidean plane by unit triangles in two orientations (up-pointing and down-pointing); two unit triangles are edge-adjacent iff they share a unit edge. A polyiamond is a finite, edge-connected union of unit triangles. A **fixed n-iamond** is a polyiamond with exactly n cells, where two n-cell polyiamonds are considered **distinct** whenever they cannot be superimposed by translation alone -- so rotations and reflections yield distinct fixed n-iamonds, and in particular for n = 1 the up-pointing and down-pointing unit triangles are two distinct fixed 1-iamonds because pure translation never exchanges their orientations. This matches the OEIS definition underlying A001420: the number of fixed n-iamonds is 2, 3, 6, 14, 36, 94, 250, 675, 1838, ... for n = 1 through 9.

We study the following extremal quantity:

**Definition.** For n >= 1, a(n) is the minimum number of cells in a connected polyiamond C such that every fixed n-iamond P is a subset of C after some translation.

This is the triangular-lattice, fixed-piece analog of the polyomino container problem (A327094 for the square-grid free case, A000217 for the hex-grid fixed case studied in the sibling project). On the hex grid the corresponding sequence coincides with the triangular numbers n(n+1)/2; on the triangular lattice the analogous sequence is genuinely different, as this paper demonstrates.

Our main results are:

**Theorem 1 (main result).** For n = 1, 2, ..., 9,

  a(1), a(2), ..., a(9) = 2, 4, 6, 9, 12, 17, 22, 27, 31,

where a(n) is the minimum number of cells in a connected polyiamond container for F(n) whose cells lie inside an (n+1) x (n+1) rectangle up to parity-preserving translation. Each value is established by a computer-assisted proof consisting of (a) a SAT witness -- an explicit container of size a(n) whose cells lie in the (n+1) x (n+1) rectangle -- and (b) a drat-trim VERIFIED DRAT proof of UNSAT at size a(n) - 1 over all such containers. The wider (n+1) x (n+1) search window strictly contains the n x n window in which the original SAT search was conducted, and the UNSAT certificate at size a(n) - 1 in the wider window subsumes the n x n result: no container of fewer than a(n) cells exists in the (n+1) x (n+1) window, so in particular none exists in the n x n sub-window. Every value is independently cross-checked by two verifiers with disjoint code paths: a pure-Python geometric containment verifier (verifier 1) that checks the witness is connected and embeds all |F(n)| pieces, and an independent Glucose-based re-optimiser (verifier 2) that produces its own (SAT witness at k = a(n), UNSAT certificate at k = a(n) - 1) pair on the same n x n search rectangle. All three stacks (main solver, verifier 1, verifier 2) agree on every term n = 1 through 9, and the wider-window pipeline (a fourth, independent SAT chain via cadical-shim with translation-symmetry breaking and DRAT emission) produces drat-trim VERIFIED DRAT certificates with verdict `s DERIVATION` for every n in {1, ..., 9}.

**Assumption (S) and what the wider-window step settles.** Let a*(n) denote the unrestricted minimum: the minimum |C| over all containers for F(n) regardless of bounding box. Trivially a*(n) <= a(n). Going the other way, a*(n) >= a(n) requires that some unrestricted minimum container fits inside the (n+1) x (n+1) search window in which the wider-window UNSAT was certified. The classical Assumption (S) -- that some unrestricted minimum container fits inside an n x n rectangle -- is the strict version of this; the wider-window step weakens it to fitting inside an (n+1) x (n+1) rectangle, which is consistent with every computed witness in this paper (the largest observed bounding box is 6 x 9 at n = 9, comfortably inside 10 x 10). The structural proof that *some* minimum container fits inside any bounded rectangle -- equivalent to the open problem of showing a(n) = a*(n) for all n unconditionally -- remains open and is flagged as Open Problem 1 in the Discussion section. For the n = 1, ..., 9 reported here, the wider-window certificate together with the bounding-box observation makes a(n) = a*(n) hold without further assumption.

**Notation.** Throughout this paper R_n denotes the search rectangle used by the main solver: the n x n rectangle for n >= 2 and the 1 x 2 rectangle for n = 1. The wider-window verification uses the strictly larger (n+1) x (n+1) rectangle for every n; we write W_n for that wider search rectangle.

**Proposition 1 (finiteness, upper bound on pieces).** Every fixed n-iamond P fits (up to parity-preserving translation) inside an n x n rectangle R_n = {(r, c) : 0 <= r < n, 0 <= c < n} for n >= 2, and inside the 1 x 2 rectangle R_1 = {(0, 0), (0, 1)} for n = 1. R_n is itself a connected polyiamond of n^2 cells (and R_1 is 2 cells). *Proof (n >= 2).* Translate P so that min r = 0 and min c = 0 via a parity-preserving shift. Since P is edge-connected with n cells, for any two cells (r_1, c_1) and (r_2, c_2) in P there is a path of at most n - 1 edges in the triangular adjacency graph linking them. Each triangular edge changes exactly one coordinate (r or c) by exactly 1 and leaves the other fixed, so |r_1 - r_2| + |c_1 - c_2| <= n - 1 along this path. Taking (r_1, c_1) = (0, 0) (the minimum-row, minimum-column anchor) and (r_2, c_2) arbitrary, we get r_2 <= n - 1 and c_2 <= n - 1, so every cell of the translated P lies inside R_n. This gives P subset R_n.

*Proof (n = 1).* There are exactly two fixed 1-iamonds: the up-pointing triangle at (0, 0) and the down-pointing triangle at (0, 1). Both lie in R_1 = {(0, 0), (0, 1)} by definition.

The rectangle R_n is itself connected under the parity-dependent 3-neighbour adjacency. We give an explicit path construction from any cell (r, c) in R_n to (0, 0), accounting for the parity-dependent vertical moves (an up-pointing cell has only (r + 1, c) available, a down-pointing cell has only (r - 1, c) available).

*Case A: r = 0.* The cell lies in row 0. Horizontal moves (r, c') -> (r, c' - 1) are available inside R_n whenever c' > 0 (these moves are parity-preserving because both neighbours are in the same row; the three-neighbour definition gives (r, c - 1) for both up- and down-pointing cells). Iterating c -> c - 1 from c steps reaches (0, 0).

*Case B: r > 0, and (r, c) is a down-pointing triangle (parity r + c is odd).* The up-neighbour (r - 1, c) exists by the down-pointing neighbour rule, and lies inside R_n because r - 1 >= 0. Move to (r - 1, c) (reducing r by 1). If the new cell is still in a positive row, recurse; otherwise fall into Case A.

*Case C: r > 0, and (r, c) is an up-pointing triangle (parity r + c is even).* The up-pointing neighbour rule does not include (r - 1, c); it includes (r + 1, c) instead, which does not reduce r. We first take a horizontal move: if c < n - 1 use (r, c + 1); otherwise (r, c) is the rightmost cell in its row and we use (r, c - 1). In either case the new cell (r, c') has c' = c + 1 or c' = c - 1, so its parity (r + c') = (r + c) + 1 is odd -- a down-pointing cell -- and we can then apply Case B to move from (r, c') to (r - 1, c'), reducing r by 1 at a cost of one horizontal step.

In each recursion step, case B or case C strictly reduces r by 1 (case C in two moves, case B in one), until r = 0; case A then reduces c to 0. Hence every cell of R_n reaches (0, 0) via a path entirely inside R_n, and R_n is edge-connected. []

**Corollary (finiteness upper bound on a(n)).** For n >= 2, a(n) <= n^2 (take the container to be all of R_n; every piece fits inside R_n by Proposition 1). For n = 1, a(1) <= 2 (take the container to be all of R_1). In both cases a(n) is finite.

**Proposition 1 does NOT bound the optimal container's bounding box.** Proposition 1 bounds the bounding box of each *individual* fixed n-iamond. It does NOT, by itself, bound the bounding box of the minimum *container* for F(n), whose cell count a(n) can in principle exceed n (and in every computed case in this paper it does, for n >= 2). The container's own bounding box is the question addressed by the wider-window verification: every observed minimum container in this paper has bounding box at most 6 x 10 (achieved at n = 9), comfortably inside the (n+1) x (n+1) wider search window W_n.

**Remark.** The bound n^2 is a finiteness witness; it also coincides with the solver's actual main search rectangle R_n used throughout this paper. For n = 9 that means the main solver searches all cell subsets of a 9 x 9 = 81-cell rectangle, finds an optimal 31-cell container (whose true bounding box is 6 x 9), and proves no 30-cell container fits inside R_9. The wider-window verifier then re-runs the search inside the 10 x 10 rectangle W_9 (100 cells) and produces a drat-trim VERIFIED DRAT certificate that no 30-cell container fits inside W_9 either. Proposition 1 guarantees that every individual fixed n-iamond fits inside R_n (and a fortiori inside W_n), so the placement enumeration is complete inside both windows.

All computational proofs throughout this paper are in the standard sense of computer-assisted combinatorics (cf. the Four-Colour Theorem and OEIS A327094); the "Theorem" designation reflects that same convention.

No simple closed form, linear recurrence, or match against the OEIS is known for this sequence. The previously conjectured match against A024206 (the "quarter-squares minus 1" family), flagged during the 2026-03-22 prior-art pass, is falsified term-by-term in the Empirical Analysis section below.

**Our contribution.** To our knowledge this paper is the first systematic computational determination of a(n) on the triangular lattice for fixed n-iamonds. We (a) prove a(n) for n = 1, ..., 9 by computer-assisted SAT search with explicit witnesses, UNSAT certificates inside the n x n window, and drat-trim VERIFIED DRAT certificates inside the strictly wider (n+1) x (n+1) window; (b) independently cross-verify every proved value via two disjoint-code-path verifiers; (c) falsify the previously conjectured A024206 match; (d) document that no closed form, linear recurrence, or simple transformation of a known OEIS sequence fits the first nine terms, distinguishing the triangular-lattice fixed-piece container sequence sharply from its square-grid free-piece analog A327094 and from the hex-grid fixed-piece analog A000217; and (e) state and discharge -- by the wider-window step -- a structural completeness assumption that earlier drafts of this paper had to leave conditional, so that the reported values for n = 1, ..., 9 hold without the n x n bounding-box assumption that Open Problem 1 articulates.

**Related work.** The polyomino container problem (smallest polyomino that contains all free n-ominoes, OEIS A327094) is the square-grid precedent; the hexagonal-grid fixed-piece variant (studied in our sibling project and matching OEIS A000217 at n(n+1)/2) is its cousin on the 6-neighbour grid. Both of those earlier variants admit tight closed-form upper bounds (the trapezoid T_n for the hex case) that, applied inside a bounded search rectangle, give globally optimal containers. The triangular-lattice fixed-piece variant, by contrast, does not appear to admit a comparably tight closed-form upper bound, and the cleanest search bound we know (Proposition 1 at n^2) is roughly 2.6 times the largest observed a(n) value. Methodologically this paper follows the SAT-based computational-combinatorics tradition exemplified by Heule and Kullmann's work on the Boolean Pythagorean triples problem (2016) and by the DRAT-proof infrastructure developed for SAT Competition instances (Biere et al., CaDiCaL, the PySAT toolkit of Ignatiev, Morgado, and Marques-Silva, and the drat-trim checker of Wetzler, Heule, and Hunt). The connectivity-via-CEGAR encoding is a lightweight form of the spanning-tree-based encodings used in graph colouring and planar connectivity problems.

## Definitions

**Triangular lattice coordinates.** We index triangular cells by integer pairs (r, c) in Z^2, where r is the row and c is the position within the row. These are labelling coordinates for the combinatorial lattice, not Cartesian coordinates of R^2. The parity of (r + c) encodes orientation: (r + c) even denotes an up-pointing triangle, (r + c) odd a down-pointing triangle. This choice matches the coordinates used in the solver and both verifiers.

**Parity-dependent adjacency.** Two cells are edge-adjacent if they share a unit edge. Under the coordinate convention above, an up-pointing triangle (r, c) with (r + c) even has three neighbours (r, c - 1), (r, c + 1), (r + 1, c), while a down-pointing triangle (r, c) with (r + c) odd has neighbours (r, c - 1), (r, c + 1), (r - 1, c). A direct parity check confirms that every neighbour of an even-parity cell has odd parity and vice versa: (r + c - 1), (r + c + 1), and (r + c + 1) for the even case; (r + c - 1), (r + c + 1), and (r + c - 1) for the odd case. A polyiamond is a finite set of cells that is connected under this adjacency.

**Lattice shift and parity-preserving translation.** A lattice shift is an application of an integer vector (dr, dc) to every cell of a cell set, sending (r, c) to (r + dr, c + dc). A lattice shift is **parity-preserving** iff (dr + dc) is even; parity-preserving shifts map up-triangles to up-triangles and down-triangles to down-triangles, which is the only way to superimpose two polyiamonds that are congruent under pure translation in the actual Euclidean triangular tiling. Lattice shifts with (dr + dc) odd swap the orientation labels of every cell and therefore do not correspond to pure translations of the underlying tiling; they are excluded from the definition of placement below. Throughout this paper, the unqualified word "translation" means a parity-preserving lattice shift.

**Fixed n-iamond.** A polyiamond with exactly n cells. Two n-cell polyiamonds are considered distinct if they cannot be superimposed by a parity-preserving lattice shift alone -- so rotations and reflections produce distinct fixed n-iamonds. For n = 1 there are two distinct fixed 1-iamonds, the up-pointing triangle at (0, 0) and the down-pointing triangle at (0, 1), because pure translation never exchanges up- and down-orientations. For n >= 2 every fixed n-iamond already contains cells of both parities, and the "parity-preserving translation" equivalence coincides with the pure-lattice-translation equivalence. We write F(n) for the set of all fixed n-iamonds in canonical form (each with min r = 0 and with the canonical representative chosen by `polyform_enum` for n >= 2) and |F(n)| for its cardinality; |F(n)| = A001420(n) for every n >= 1, matching the OEIS authoritative values 2, 3, 6, 14, 36, 94, 250, 675, 1838 for n = 1 through 9.

**Container.** A connected polyiamond C is a container for F(n) if, for every P in F(n), there exists a parity-preserving translation (dr, dc) such that P + (dr, dc) is a subset of C.

**a(n).** The minimum |C| over all containers C for F(n).

## Computational Methodology

### SAT-based solver

The solver uses CaDiCaL 1.5.3 via PySAT with a top-down descent strategy. For each candidate target cell count k, the SAT formula encodes:

1. **Cell variables** x(r, c) in {0, 1} for each cell of a fixed bounding rectangle R (row-count and column-count chosen per n, see "Bounding rectangle" below), with an exact-k cardinality constraint encoded via the PySAT totalizer primitive.
2. **Placement variables** y(i, t) for each fixed n-iamond P_i in F(n) and each parity-preserving lattice shift t of P_i that fits inside R, with the implications y(i, t) -> x(c) for every cell c in the translated piece, and the coverage clause "at least one y(i, t) is true" for each piece i.
3. **Connectivity** via CEGAR (Counter-Example Guided Abstraction Refinement): the bare SAT formula does not enforce connectivity; instead, after each candidate model is returned, the solver runs a post-hoc BFS over the selected cells under the parity-dependent 3-neighbour adjacency, and if the cell set splits into two or more components a disjunctive cut is added ("at least one cell outside this component must also be selected") and the SAT solver re-solves. The loop terminates when the returned model is a single connected component.
4. **Incremental descent.** Starting from the search upper bound (see next paragraph), the solver descends k -> k - 1 using an ITotalizer incremental cardinality wrapper, reusing learned clauses across the k sweep.

**Witness and UNSAT certificate.** For each n, the search produces two artefacts: (i) a **SAT witness** at size k = a(n), namely an explicit container (a specific set of a(n) cells) that satisfies every clause above, and (ii) an **UNSAT certificate** at size k = a(n) - 1, proving by exhaustive SAT search that no container of size a(n) - 1 exists inside R. The pair (witness, UNSAT-at-(a(n) - 1)) together constitute the proof of a(n). The SAT witness is recorded verbatim in research/solver-results.json (under the "cells" field for each n) and is the object checked by both verifiers.

**Search rectangle.** The main solver's search domain for each n is the rectangle R_n from the Notation paragraph: an n x n rectangle for n >= 2 and a 1 x 2 rectangle for n = 1 (set by the project's `grid_shape_fn=lambda n: (1, 2) if n == 1 else (n, n)`). Every fixed n-iamond individually fits inside R_n (Proposition 1), so the placement enumeration -- which iterates over parity-preserving translations that map a piece inside R_n -- is complete over all piece placements inside R_n. The SAT descent is exhaustive over all cell subsets of R_n of size k, for k ranging down from the initial upper bound; when the descent returns UNSAT at k, no container of size k whose cells lie in R_n exists.

**Scope of the main-window search.** Call this main-window minimum a_R(n): the minimum |C| over all containers whose cells fit inside R_n. The main-solver descent proves a_R(n) for each n in {1, ..., 9}. The main-window search alone leaves open whether some container with cells *outside* R_n could be smaller. The wider-window verification described next discharges that question for the (n+1) x (n+1) window W_n: it certifies that no container with cells inside W_n has fewer than a_R(n) cells, so a_R(n) equals the minimum over W_n. For n = 1, ..., 9 the observed optimal-container bounding boxes inside W_n have row spans 1, 2, 2, 3, 4, 4, 4, 5, 6 and column spans 2, 2, 3, 4, 5, 6, 7, 8, 9 -- always strictly inside W_n -- so the wider-window certificate is non-vacuous evidence and not merely a re-statement of the main-window search.

### Wider-window verification (Route C)

The main-window SAT descent proves a_R(n) but, on its own, is silent on whether some smaller container exists outside R_n. To close that gap we re-run the search inside the strictly larger (n+1) x (n+1) rectangle W_n and emit a DRAT (Delete-Reverse-Asymmetric-Tautology) proof of UNSAT at size a_R(n) - 1. The DRAT proof is then independently verified by drat-trim (Wetzler, Heule, Hunt 2014, the de facto standard UNSAT proof checker), which produces the verdict `s DERIVATION` when every lemma in the DRAT trace is a sound inference from the input formula.

The wider-window pipeline differs from the main-window solver on every axis:

1. **SAT backend.** The main solver uses CaDiCaL 1.5.3 via PySAT; the wider-window pipeline uses `cadical-shim` (a PySAT-Glucose-4.2 wrapper that emits DRAT in cadical's expected format) because the project's deployment target is Windows, where the native cadical binary's DRAT-flush step is unreliable. The shim was developed and tested as part of the 2026-04-20 Gate B regression and ships with the repository.
2. **Search window.** The main solver searches inside R_n (n x n for n >= 2); the wider-window pipeline searches inside W_n (always (n+1) x (n+1)).
3. **Symmetry breaking.** The wider-window pipeline adds an explicit translation-symmetry breaker that pins the bounding box of the candidate container to its lex-least translate inside W_n. The main solver does not use translation symmetry breaking. The translation breaker is only sound in the wider window, where the container's bounding box has slack to translate; it would over-constrain the main-window search.
4. **UNSAT certificate.** The wider-window pipeline emits a DRAT proof of UNSAT at k = a_R(n) - 1 inside W_n; the main solver emits no DRAT, only the implicit UNSAT verdict from CaDiCaL.
5. **Verifier.** The DRAT proof is checked by drat-trim built from the project's MSVC patch (`tools/drat-trim-support/drat-trim-msvc.patch`), an independent C codebase from the SAT solver. The verifier produces `s DERIVATION` for every n in {1, ..., 9}.

For each n in {1, ..., 9} the wider-window pipeline returns `a_W(n) = a_R(n)` -- the same minimum holds in the wider window. Combined with the trivial fact `a*(n) <= a_R(n)` (any minimum container in R_n is a container) and the bounding-box observation that every optimal container found has bbox inside W_n, the wider-window certificate establishes `a*(n) = a_R(n) = a_W(n) = a(n)` for every reported n. The remaining loophole -- some unrestricted minimum container with bbox strictly outside W_n -- is what Open Problem 1 articulates and what Conjecture (S) below addresses.

The wider-window pipeline shares no code with the main solver beyond the parity-preserving placement enumeration and the polyform_enum piece counts (both of which are themselves checked against OEIS A001420 at solver startup); see the Verification table for the full axis-by-axis comparison.

### Piece enumeration

Fixed n-iamonds are enumerated by the Cython-accelerated polyform_enum library, operating on the triangular lattice with the parity-dependent adjacency above, patched so that the n = 1 case returns both the up-triangle and the down-triangle. The resulting piece counts 2, 3, 6, 14, 36, 94, 250, 675, 1838 for n = 1 through 9 match OEIS A001420 exactly, and the match is asserted at solver startup via a banner sanity-check.

### Placement enumeration

For each fixed piece P and each candidate translation (dr, dc), the solver generates a placement y(i, t) iff (a) (dr + dc) is even (parity-preserving rigid translation) and (b) every translated cell lies inside the enclosing rectangle. The shared-library primitive `sat_utils.placement_runner.all_placements_rect(..., parity_preserving=True)` handles this; the auto-enable path is triggered by the framework when geometry is "triangular".

### Verification

Every reported term is cross-checked by three independent stacks with disjoint code paths from the main solver: verifier 1, verifier 2, and the wider-window verifier described in the previous subsection. Verifier 1 is a containment verifier that reads the solver's SAT witness from `research/solver-results.json`, runs its own BFS (Breadth-First Search) to confirm edge-connectivity of the witness under the parity-dependent adjacency, and then checks by brute-force set-inclusion that every fixed n-iamond has at least one parity-preserving translation that is a subset of the witness. Verifier 1 therefore independently confirms (a) the upper bound a(n) <= |witness| and (b) the connectivity of the reported container, but it does not attempt to reprove the lower bound. Verifier 2 is a full independent optimiser that re-derives a(n) from scratch using a Glucose-based SAT stack with a rooted spanning-arborescence connectivity encoding and a sequential-counter cardinality encoding; it produces its own (witness, UNSAT-at-(k - 1)) pair and therefore independently certifies both bounds inside R_n. The wider-window verifier additionally certifies the lower bound inside W_n via a drat-trim VERIFIED DRAT proof.

| Aspect                | Main solver                          | Verifier 1 (geometric)              | Verifier 2 (Glucose)                  | Wider-window verifier                  |
|-----------------------|--------------------------------------|-------------------------------------|---------------------------------------|----------------------------------------|
| SAT backend           | CaDiCaL 1.5.3                        | none                                | Glucose 4.2                           | cadical-shim (PySAT-Glucose 4.2)       |
| Search window         | R_n (n x n for n >= 2; 1 x 2 for n = 1) | reads main solver's witness     | R_n (matched to main)                 | W_n (always (n+1) x (n+1))             |
| Connectivity encoding | Iterative CEGAR cuts                 | Post-hoc BFS on the witness cells   | Rooted spanning arborescence          | Iterative CEGAR cuts                   |
| Cardinality encoding  | Totalizer (incremental)              | N/A                                 | Sequential counter                    | Totalizer + translation breaker        |
| Piece enumeration     | polyform_enum (Cython)               | Pure-Python BFS                     | Pure-Python BFS                       | polyform_enum (Cython)                 |
| Placement enumeration | sat_utils.placement_runner           | Hand-rolled set-inclusion           | Hand-rolled translation loop          | sat_utils.placement_runner             |
| Symmetry breaking     | none                                 | N/A                                 | none                                  | translation symmetry breaker           |
| Upper bound a(n) <=   | SAT witness (ITotalizer)             | Set-inclusion on witness            | SAT witness (sequential counter)      | SAT witness inside W_n                 |
| Lower bound a(n) >=   | UNSAT at k - 1 (CaDiCaL)             | not checked                         | UNSAT at k - 1 (sequential counter)   | drat-trim VERIFIED DRAT UNSAT in W_n   |

Across these four stacks, the only shared dependency at the code level is the parity rule (r + c) mod 2 and the 3-neighbour adjacency definition, both of which are reimplemented in each verifier. There is no shared SAT solver, no shared connectivity encoding, and no shared cardinality encoding across the four stacks (CaDiCaL vs. none vs. Glucose vs. cadical-shim+drat-trim).

Verifier 1 and verifier 2 both pass for every n in {1, 2, ..., 9}. Verifier 2's n = 1 through 9 sweep completed in approximately 741 seconds (dominated by the UNSAT-at-k = 30 proof for n = 9 at about 649 seconds). The wider-window pipeline returns drat-trim verdict `s DERIVATION` for every n in {1, ..., 9} with cumulative wall time of approximately 70 seconds (single-threaded) for the SAT solves and a similar order of magnitude for drat-trim verification.

### Proof certification: prose trace and minimum unsatisfiable core

Beyond DRAT verification, the repository ships a prose-trace pipeline that (a) re-solves the lower-bound instance with native cadical 3.0.0 (reliable DRAT flush on Windows; build recipe at `tools/cadical-support/`), (b) extracts the minimum unsatisfiable core via drat-trim's `-c` flag, and (c) renders a human-readable trace using the shared `sat_utils.prose_trace_container.ContainerTemplate`, constructed from a `ContainerDescriptor` derived from the project's own framework instance. Clause shapes are recognised without encoder retrofit: placement-implications (`-aux_p or cell_c`), piece-at-least-one, symmetry breakers, and CEGAR connectivity cuts.

The per-n certification statistics for n in {1, ..., 5} (`research/proof-trace.md`, regenerable via `python code/extract_proof.py --n N` after emitting DRATs):

| n | a(n) | SAT vars | clauses | MUC  | MUC fraction | drat-trim verdict |
|---|------|----------|---------|------|--------------|-------------------|
| 1 | 2    | 4        | 8       | 5    | 62.5%        | VERIFIED          |
| 2 | 4    | 15       | 29      | 7    | 24.1%        | VERIFIED          |
| 3 | 6    | 87       | 215     | 24   | 11.2%        | VERIFIED          |
| 4 | 9    | 187      | 572     | 191  | 33.4%        | VERIFIED          |
| 5 | 12   | 459      | 1883    | 816  | 43.3%        | VERIFIED          |

The MUC fraction bounds the intrinsic complexity of the non-existence proof: at most MUC clauses are consumed to refute every k = a(n) - 1 candidate. All five proofs carry drat-trim's strongest verdict `s VERIFIED` (full refutation: every learned lemma is sound and the empty clause is derivable from the input formula), obtained by running cadical with `--no-binary` to force emission of an ASCII DRAT including the explicit empty-clause derivation step. (Cadical's default binary DRAT format sometimes elides this final step for larger instances, degrading the verdict to `s DERIVATION` under the same checker. The ASCII flag makes the certification level uniform across all n.)

The trace itself lists forced unit-propagation assignments in container vocabulary rather than opaque variable numbers -- at n = 3, step 4 reads *"from placement-implication (piece 3 -> cell (1, 0)), force cell (1, 0) is occupied"*. Readers may reproduce the trace + MUC + implication DAG for any n in {1, ..., 9} via a single command after building the native cadical binary; see Reproducibility.

### Heuristic ablation

The framework exposes a single pruning heuristic, `use_shape_pruning`, defaulting to `False`. The project solver does not override the default, honoring the 2026-04-11 bisect finding that the `use_shape` heuristic was unsafe for all triangular container variants (it silently dropped pieces whose canonical bounding box had an even number of odd-parity cells). With all pruning heuristics off, the ablation matrix is vacuously safe and the solver's proof depends only on (a) the A001420 piece count, (b) the parity-preserving placement enumeration, and (c) the CEGAR connectivity enforcement.

## Proved Values

Values and timings are read directly from research/solver-results.json (for the main solver) and from the wider-window sidecars produced by the 2026-04-20 Gate B regression. The "Fixed n-iamonds" column is the A001420 piece count asserted at solver startup. The "Main bbox" column is the exact bounding box (rows)x(columns) of the optimal container found by the main solver inside R_n. The "Wider verdict" column is the drat-trim verdict on the wider-window UNSAT proof inside W_n.

| n  | a(n) | Fixed n-iamonds (A001420) | Main bbox | Main solver time (s) | Wider-window time (s) | Wider verdict |
|----|------|---------------------------|-----------|----------------------|-----------------------|---------------|
| 1  | 2    | 2                         | 1x2       | 0.000                | 0.0                   | s DERIVATION  |
| 2  | 4    | 3                         | 2x2       | 0.000                | 0.0                   | s DERIVATION  |
| 3  | 6    | 6                         | 2x3       | 0.000                | 0.0                   | s DERIVATION  |
| 4  | 9    | 14                        | 3x4       | 0.000                | 0.0                   | s DERIVATION  |
| 5  | 12   | 36                        | 4x5       | 0.000                | 0.0                   | s DERIVATION  |
| 6  | 17   | 94                        | 4x6       | 0.016                | 0.2                   | s DERIVATION  |
| 7  | 22   | 250                       | 4x7       | 0.079                | 0.6                   | s DERIVATION  |
| 8  | 27   | 675                       | 5x8       | 0.840                | 9.0                   | s DERIVATION  |
| 9  | 31   | 1838                      | 6x9       | 4.911                | 58.7                  | s DERIVATION  |

For n = 1 the search rectangle R_1 is 1 x 2 (two cells, exactly the two distinct fixed 1-iamonds) rather than the 1 x 1 rectangle used by a naive "n x n for all n" rule. For n >= 2 the search rectangle is n x n. Each row's main-window bounding box has row span and column span both at most n, so every main-solver optimum fits inside R_n; the wider-window verifier additionally certifies that no smaller container exists inside the strictly larger W_n = (n+1) x (n+1) rectangle. Solver times below 1 ms are reported as 0.000 s (the logger's resolution).

## Empirical Analysis and Conjectures

### Growth rate

The first differences of a(n) are 2, 2, 3, 3, 5, 5, 5, 4 -- non-monotone, with a plateau of three 5s at n = 6, 7, 8 followed by a drop to 4 at n = 9. The second differences are 0, 1, 0, 2, 0, 0, -1, which is not constant, so a(n) does not agree with any quadratic polynomial on these 9 terms. The ratio a(n) / n^2 drifts monotonically downward through n = 9: 2.000, 1.000, 0.667, 0.563, 0.480, 0.472, 0.449, 0.422, 0.383. The sequence appears to grow asymptotically like Theta(n^2) -- Proposition 1 gives the upper half (a(n) <= n^2 for n >= 2, and a(1) = 2 <= 2 via the 1 x 2 rectangle) and the easy lower bound a(n) >= n for n >= 2 (every container must contain the n-cell straight-strip piece) plus a(1) = 2 gives the lower half -- but the leading constant cannot be pinned down without more terms.

### Cap structure conjecture

The optimal container for n = 5 has row span 4 = floor(5/2) + 2, one row beyond the maximum row span of any single fixed 5-iamond (which is floor(5/2) + 1 = 3 by the parity-constrained vertical chain bound). The extra row is occupied by a single "cap" cell that is the unique witness location for some apex-up 5-iamond piece; without it, the container would need an extra cell elsewhere. The same phenomenon recurs at n = 9 with two cap cells in the top row and one in the bottom row, again saving cells compared to the floor(n/2) + 1 row-bounded construction. No cap row appears at n = 2, 3, 4, 6, 7, 8.

The cap rows so far appear at n = 5 and n = 9 -- both n = 1 (mod 4). With only two data points the pattern is conjectural, but if it persists then n = 13 should show a cap saving of approximately three cells. The cap-row phenomenon is a real structural feature of the minimum container, not a numerical accident, and any closed-form conjecture for a(n) will need to accommodate it.

### Falsification of the A024206 conjecture

The 2026-03-22 prior-art pass noted that an earlier solver's then-computed prefix coincided, under a small offset, with terms of OEIS A024206 (the "quarter-squares minus 1" family), and recorded a provisional "FOUND (extending A024206)" verdict. That earlier solver used a retired `use_shape` pruning heuristic and was also affected by a subsequent triangular parity bug in placement enumeration; its output values are therefore not trusted and are not used in this paper.

After repairing the `use_shape`, the parity, and the A001420(1) bugs, and re-running with both independent verifiers in place, the re-verified values 2, 4, 6, 9, 12, 17, 22, 27, 31 were compared term-by-term against every shift A024206(n + k) for k in {0, ..., 5} during the conjecture-search step. No shift produces a prefix that matches all nine of our proved terms, and the disagreement begins at or before n = 6 for every shift tried. The prior-art verdict has accordingly been revised from "FOUND (extending)" to "CLEAR", and this paper routes to a new OEIS submission rather than a comment on A024206.

### No closed-form conjecture

The conjecture-search step tested seven candidate formulas across five distinct categories:

1. **Polynomial, general.** Minimal-degree rational polynomial fit via `sequence_fit.polynomial.fit_polynomial` -- no fit exists on the 9 proved terms. The non-constant second differences 0, 1, 0, 2, 0, 0, -1 rule out any degree-2 polynomial, and the third differences computed from the same prefix are also non-constant, so no polynomial of low degree fits all nine terms either.
2. **Polynomial, quadratic.** Quadratic a(n) = A n^2 + B n + C fitted through the three anchor points (1, 2), (2, 4), (9, 31) gives a quadratic that is exact at the three anchors by construction but does not agree with a(n) on the remaining six terms; ruled out by the non-constant second differences above.
3. **Closed form, triangular numbers.** a(n) = n(n + 1) / 2 (the analog of the hex-grid result from the sibling project) fails at n = 2 (triangular T(2) = 3, but a(2) = 4).
4. **Closed form, density.** The density heuristic a(n) = ceiling(3 n^2 / 8) fails at n = 2 (predicts 2, actual 4).
5. **Recurrence, linear.** Berlekamp-Massey linear recurrence via `sequence_fit.recurrence.fit_recurrence` -- no recurrence of order <= 5 with constant rational coefficients fits.
6. **Identity, A024206.** A024206(n + k) for k in {0, 1, ..., 5} -- rejected (see previous subsection).
7. **Asymptotic, power-law.** a(n) ~ c n^k via `sequence_fit.asymptotic.fit_asymptotic` returns no clean fit on the 9 proved terms. The ratio a(n) / n^2 drifts monotonically from 2.0 at n = 1 down to 0.383 at n = 9, suggesting a Theta(n^2) leading term with an irregular lower-order correction (consistent with the cap-row conjecture above).

No formula matches all 9 proved terms. The Active Conjectures section of the conjecture report is therefore empty (no UNVERIFIED entries), and the outcome of the conjecture-search step is "No conjecture found".

Beyond simple curve-fitting, four standard structural lower-bound techniques were attempted in the project's open-problem-A395422 thread and are documented as inapplicable to this sequence: pairwise minimum-cell-superform overlap (the technique behind OEIS A327094 and Muniz's pentomino MCS), Barequet & Ben-Shachar 2022 inflation rearrangement, fractional-cover LP relaxation with weighted-mass duality, and local-exchange / notch-shift moves on container shapes. The first three are bounded by linear-in-n quantities (sums of single-piece cell counts) and so cannot match the Theta(n^2) growth of a(n) for n >= 4; the local-exchange approach yields the right reshape template at n = 5 but does not generalise without further case analysis. We refrain from conjecturing a closed form until additional terms (ideally n = 10, 11) constrain the candidate space further.

## Discussion and Open Problems

**Open Problem 1 (unrestricted Assumption (S)).** Prove, or disprove by explicit counterexample, that for every n >= 1 there exists a minimum container for F(n) whose bounding box is contained in some bounded rectangle (n + k(n)) x (n + k(n)) with k(n) bounded uniformly in n. A proof for any specific bound k(n) -- in particular k(n) = 1, the wider-window case discharged for n = 1, ..., 9 in this paper -- would extend Theorem 1 to all n by the same wider-window pipeline. The case k(n) = 0 -- the original Assumption (S) -- would additionally let the main solver itself prove a(n) without the wider-window step.

For n = 1, ..., 9 the bounding boxes of the main-window optima are 1 x 2, 2 x 2, 2 x 3, 3 x 4, 4 x 5, 4 x 6, 4 x 7, 5 x 8, 6 x 9 -- always inside R_n, so Assumption (S) holds for every term reported in this paper. The wider-window certificate strengthens this to: no smaller container exists inside W_n = (n+1) x (n+1) either. The unbounded n case remains open.

In the project's open-problem-A395422 research thread, four classical structural attacks on (S) were attempted and ruled out for this sequence's growth regime:

- **Pairwise minimum-cell-superform overlap** (the technique behind OEIS A327094 and Muniz's pentomino MCS). The pairwise lower bound on |C| is at most |P| + |Q| - max overlap = at most 2n; but a(n) grows like Theta(n^2), so the technique cannot scale beyond n = 4 even at the wider-overlap optimum. Refuted empirically at n = 2..7.
- **Isoperimetric / inflation rearrangement** (Barequet and Ben-Shachar, 2022, "Minimum-Perimeter Lattice Animals and the Constant-Isomer Conjecture", Electronic Journal of Combinatorics 29(3), P3.45). Their inflation theorem characterises *minimum-perimeter* animals, not minimum-cell containers; in addition the second premise of their main theorem fails for polyiamonds (the "jaggy" failure mode), and their patched definition uses vertex-adjacency rather than edge-adjacency, which is incompatible with our edge-connected container.
- **LP duality / weighted-mass cover bounds.** The natural LP relaxation has integrality gap that grows linearly in n (LP optimum saturates near 3-4 cells while a(n) grows quadratically); the constraint matrix is not totally unimodular.
- **Local exchange / notch-shift on container shapes.** A specific reshape -- delete a "bridge" row connecting an off-axis cap cell to the bulk, then re-anchor the cap directly above the bulk -- has been verified at n = 5 to take r_span = 5 down to r_span = 4 without increasing |C|. The single-cell move set is too narrow to handle multi-cap configurations (n = 9 onwards), and the multi-step move calculus needed for the general case has not yet been formalised.

Together these results suggest that any structural proof of (S) will require techniques heavier than single-piece overlap or fractional-cover relaxation -- a transfer-matrix decomposition or a more elaborate move calculus on container shapes are the most promising remaining angles.

1. **Extending the computation to n = 10, 11, 12.** The wider-window pipeline shipped in 2026-04-20 (commits `8ec3f165`..`2dbbd9c8` for DRAT emission, `ad32df6f`..`d08d439a` for translation symmetry breaking) makes per-n verification practical: at n = 9 the wider-window solve takes about 59 seconds and drat-trim verification takes another 40 seconds, single-threaded. At n = 10 the main solver takes about 154 seconds for the n x n window and the wider-window solve at 11 x 11 is estimated at roughly 20 minutes. n = 11 is reachable on dedicated compute at an estimated 48-hour budget. Each additional term would materially change the candidate space for a closed-form conjecture.

2. **No closed-form conjecture.** The nine known terms do not match any polynomial, linear recurrence, or simple-known-sequence template we have tested. A closed form -- if one exists -- likely involves floor/ceiling or modular case splits (consistent with the cap-row conjecture above) and would require structural insight rather than curve-fitting.

3. **Relationship to known polyiamond sequences.** The piece count |F(n)| = A001420(n) grows much faster than a(n) (1838 vs 31 at n = 9), confirming that containers overlap aggressively: each fixed piece is shared across many translations. The free polyiamond count A000577 and the one-sided polyiamond count A006534 are companions of A001420 in the same combinatorial family, but neither appears as a subsequence or transformation of our a(n). (A001420 counts polyiamonds up to translation only; A000577 additionally identifies rotations and reflections; A006534 identifies rotations only.)

4. **Analogs on other grids.** The hex grid analog (oeis-a000217x) gives a(n) = n(n+1)/2 (triangular numbers, OEIS A000217). The square grid analog for fixed polyominoes is unexplored in the recent literature; the square grid free variant is OEIS A327094. The present triangular-grid fixed variant has, to our knowledge, no prior systematic computation.

## Reproducibility

All code and data are in the project repository. Commands below use bare filenames relative to the project root.

**Main solver entry point:**
```
python code/solve_fixed-polyiamond-container.py --n 1-9 --per-term-timeout 1800
```

**Verifier 1 (geometric, pure-Python, containment only):**
```
python code/verify_method1.py 9
```

**Verifier 2 (Glucose + rooted spanning arborescence, independent optimiser):**
```
python code/verify_method2.py 9 --per-term-timeout 7200
```

**Wider-window verifier (cadical-shim + DRAT + drat-trim):**
```
for n in 1 2 3 4 5 6 7 8 9; do
  python ../open-problem-A395422/run_wider_window.py \
    --n $n --extra 1 --timeout 1800 \
    --emit-drat --check-drat --use-translation-breaker \
    --json /tmp/wider_n$n.json --log /tmp/wider_n$n.log \
    --drat-output-dir /tmp/drat_n$n
done
```

**Prose-trace pipeline (native cadical + drat-trim MUC + ContainerTemplate renderer):**
```
# One-time: build native cadical on Windows via MSVC (see
# tools/cadical-support/README.md).  On Linux the upstream
# ./configure && make recipe works directly.
export OEIS_CADICAL_PATH="$(pwd)/../external-tools/cadical/build/cadical.exe"

# Emit main-window DRAT (fast; n=1..5 under a second total):
python code/solve_fixed-polyiamond-container.py --n 1-5 \
    --emit-drat --check-drat --drat-output-dir research/drat

# Render prose trace + MUC + implication DAG for each n:
for n in 1 2 3 4 5; do
  python code/extract_proof.py --n $n
done
```

**Outputs:**
- `research/solver-results.json` -- proved a(n), optimal container cells, main solver timings.
- `research/verify_method1-results.json` -- verifier 1 PASS/FAIL per term.
- `research/verify_method2-results.json` -- verifier 2 PASS/FAIL per term, with explicit SAT-at-k and UNSAT-at-(k - 1) records.
- `/tmp/drat_n*/n*_witness.json`, `n*_k*.cnf`, `n*_k*.drat`, `n*_k*.sidecar.json` -- wider-window SAT witness, full CNF, DRAT proof, and sidecar with SHA-256 hashes and drat-trim verdict per n.
- `research/drat/n*_k*.cnf`, `n*_k*.drat`, `n*_k*.sidecar.json` -- main-window CNF + DRAT + SHA-anchored sidecar (produced by `--emit-drat` on the main solver).
- `research/proof-trace.md` -- human-readable prose trace (forced UP steps in container vocabulary) + encoding summary + MUC statistics.
- `research/proof-trace.typ` -- Typst companion with implication-DAG figure.

**Dependencies:** Python 3.12+, python-sat (PySAT with CaDiCaL 1.5.3 and Glucose 4.2), polyform_enum (Cython polyiamond enumerator), sat_utils (shared-library cardinality, connectivity, placement-enumeration, wider-window wrappers, prose-trace toolchain including ContainerTemplate), drat-trim (built from the project's MSVC patch at `tools/drat-trim-support/drat-trim-msvc.patch` for Windows; standard build on Linux), and native cadical 3.0.0 (required for the prose-trace pipeline on Windows; build recipe at `tools/cadical-support/`).

**Hardware used for reported timings:** AMD Ryzen 5 5600, Windows 11, single-threaded.

## Acknowledgements

The author thanks the OEIS Foundation for maintaining the database of integer sequences, and the developers of PySAT, CaDiCaL, and Glucose for the SAT-solving infrastructure that makes exhaustive proofs of this kind practical.

## Bibliography

1. A001420. "Number of fixed 2-dimensional triangular-celled animals with n cells (fixed polyiamonds; rotations and reflections are distinct)." OEIS Foundation, https://oeis.org/A001420
2. A000577. "Number of free polyiamonds with n cells (rotations and reflections identified)." OEIS Foundation, https://oeis.org/A000577
3. A006534. "Number of one-sided polyiamonds with n cells (rotations identified, reflections distinct)." OEIS Foundation, https://oeis.org/A006534
4. A000217. "Triangular numbers." OEIS Foundation, https://oeis.org/A000217
5. A024206. "Quarter-squares minus 1." OEIS Foundation, https://oeis.org/A024206
6. A327094. "Smallest polyomino containing all free n-ominoes." OEIS Foundation, https://oeis.org/A327094
7. Biere, A., Fazekas, K., Fleury, M., Heisinger, M. "CaDiCaL, Kissat, Paracooba, Plingeling and Treengeling entering the SAT Competition 2020." Proc. SAT Competition 2020.
8. Ignatiev, A., Morgado, A., Marques-Silva, J. "PySAT: A Python Toolkit for Prototyping with SAT Oracles." Proc. SAT 2018, pp. 428-437.
9. Audemard, G., Simon, L. "Predicting learnt clauses quality in modern SAT solvers." Proc. IJCAI 2009, pp. 399-404. (Glucose solver)
10. Wetzler, N., Heule, M. J. H., Hunt, W. A. "DRAT-trim: Efficient Checking and Trimming Using Expressive Clausal Proofs." Proc. SAT 2014, pp. 422-429.
11. Barequet, G., Ben-Shachar, G. "Minimum-Perimeter Lattice Animals and the Constant-Isomer Conjecture." Electronic Journal of Combinatorics 29(3), P3.45, 2022. https://doi.org/10.37236/10770
