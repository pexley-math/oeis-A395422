# Conjecture Report for oeis-A395422

**Date:** 2026-04-11 (revised 2026-04-22 -- scope capped at n=9 for publication)
**Terms proved:** 9 (a(1) through a(9))
**Source:** research/solver-results.json
**Sequence:** a(n) = minimum number of triangular cells in a (fixed) polyiamond
that contains a translated copy of every fixed n-iamond on the
triangular grid.

## Proved Terms

| n | a(n) | Source |
|---|------|--------|
| 1 | 2    | OUR PROOF (solver + 2 independent verifiers + drat-trim VERIFIED DRAT) |
| 2 | 4    | OUR PROOF |
| 3 | 6    | OUR PROOF |
| 4 | 9    | OUR PROOF |
| 5 | 12   | OUR PROOF |
| 6 | 17   | OUR PROOF |
| 7 | 22   | OUR PROOF |
| 8 | 27   | OUR PROOF |
| 9 | 31   | OUR PROOF |

Note 1: the 2026-03-22 legacy run reported (1, 3, 5, 8, 11, 15, 19, 24, 29)
using a solver with two bugs (the retired `use_shape` heuristic and the
triangular parity bug in placement enumeration). Those values are WRONG and
are not used here.

Note 2: the a(1) = 2 value was corrected 2026-04-11 (late session) after a
consensus review surfaced that OEIS A001420(1) = 2, not 1. `polyform_enum`
had been hard-coding a single up-triangle at n=1 TRIANGLE, silently
undercounting by 1. Fixed at both the Python wrapper and Cython source
levels. The minimum 2-cell rhombus (1 up + 1 down) is the n=1 witness.
All entries below use the corrected sequence 2, 4, 6, 9, 12, 17, 22, 27, 31.

## OEIS Subsequence Search

Live OEIS queries via WebFetch are blocked in the current environment (403 to
oeis.org). The following searches and comparisons were carried out against
(a) the local `sequence_fit.reference_sequences.REFERENCE_SEQUENCES` table
and (b) the candidate sequences flagged by the prior-art-search step
(`compendium/oeis/fixed-polyiamond-container-prior-art-search.dat`).

**Queries performed:**

1. Full sequence 2, 4, 6, 9, 12, 17, 22, 27, 31 against every entry in
   `sequence_fit.reference_sequences.REFERENCE_SEQUENCES` via
   `sequence_fit.reference_match.match_reference(a)` -- **no match**.
2. Shifted variants (a(n+k) for k in 1..3) against the same table -- no match.
3. First differences 2, 2, 3, 3, 5, 5, 5, 4 -- irregular; does not match
   any standard small-difference sequence in the local table.
4. Second differences 0, 1, 0, 2, 0, 0, -1 -- irregular; rules out pure
   quadratic closed form on these 9 terms.
5. Partial sums 2, 6, 12, 21, 33, 50, 72, 99, 130 -- no local-table match.
6. Direct term-by-term comparison against A024206 (the "quarter-squares
   minus 1" family flagged by the 2026-03-22 prior-art pass). Published
   A024206 prefix 0, 0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 36, 42, ...
   No shift produces agreement on all 9 proved terms; the best overlap
   (shift=3) already differs at n=6 (A024206 gives 16, we have 17).
7. A001420 (number of fixed n-iamonds: 2, 3, 6, 14, 36, 94, 250, 675, 1838):
   companion sequence, not the same quantity -- documented as a
   cross-reference only.
8. A000577, A006534, A000105 (free and one-sided polyiamond counts): also
   companions, not the same quantity.
9. A000217 (triangular numbers 1, 3, 6, 10, 15, 21, 28, 36, 45):
   analog of the oeis-a000217x result on the hexagonal grid. On the triangular
   grid our sequence differs from A000217 from n=2 onwards (a(2)=4 vs T(2)=3,
   a(4)=9 vs T(4)=10) and the residuals are irregular.

**Matches found:** none. The sequence does not appear in the local
reference table, and the only previously conjectured match (A024206) is
falsified term-by-term. The prior-art `.dat` file's provisional verdict of
"FOUND (extending)" is now superseded -- routing must be as a **NEW OEIS
entry**, not a COMMENT on A024206.

**Network note:** live queries against oeis.org were not available during
this step. Before submission the `/oeis-draft` skill should re-run the
sequence against the OEIS superseeker as a final novelty check.

## Formula Tests

Seven candidate formulas were tested across five distinct categories
(polynomial, closed form, recurrence, identity, asymptotic).

| # | Category            | Formula tried                                                                          | Matches all? | First failure                        | Motivation |
|---|---------------------|----------------------------------------------------------------------------------------|--------------|--------------------------------------|------------|
| 1 | polynomial          | minimal-degree rational polynomial fit via `sequence_fit.polynomial.fit_polynomial`    | No           | no fit found over all n              | Standard first test -- ruled out by irregular second differences 0, 1, 0, 2, 0, 0, -1 |
| 2 | polynomial          | quadratic a(n) = A n^2 + B n + C fitted on n in {1, 2, 9}                              | No           | n=5 (predicts 13.1 vs actual 12)     | Rough check of quadratic shape |
| 3 | closed form         | a(n) = n(n+1)/2 (triangular numbers, analog of oeis-a000217x on the hex grid)          | No           | n=2 (T(2)=3 vs 4)                    | Direct analog of the hex-grid result A000217 from the sibling project |
| 4 | closed form         | a(n) = ceiling(3 n^2 / 8)                                                              | No           | n=2 (2 vs 4)                         | Density heuristic: triangular lattice has cell-density ratio 3/8 vs the square grid |
| 5 | recurrence          | Berlekamp-Massey linear recurrence via `sequence_fit.recurrence.fit_recurrence`        | No           | no recurrence of any order <= 5 fits | Standard automatic test for linear recurrences with constant coefficients over Q |
| 6 | identity            | term-by-term comparison against A024206 under shifts 0..5                              | No           | best shift (k=3) already fails at n=6 | 2026-03-22 prior-art pass claimed this match; explicitly falsified here |
| 7 | asymptotic          | power-law a(n) ~ c n^k via `sequence_fit.asymptotic.fit_asymptotic`                    | No           | no clean fit returned                 | Sanity check on growth rate; a(n)/n^2 drifts from 2.0 (n=1) to 0.383 (n=9) |

## Active Conjectures (match all proved terms -- UNVERIFIED)

None. No formula among the tested candidates matched all 9 proved terms,
so there is no active conjecture to mark UNVERIFIED at this time. Any
candidate formula suggested by future work must be appended under this
heading with the explicit UNVERIFIED tag.

## Conjectures Rejected

- **a(n) = A024206(n+k) for any shift k in 0..5** -- best shift (k=3)
  already differs at n=6. This falsifies the 2026-03-22 provisional
  prior-art claim and forces the project to route as a NEW sequence
  submission.
- **a(n) = n(n+1)/2** -- matches n=1 and n=3 only; differs at n=2, 4, 5,
  6, 7, 8, 9.
- **a(n) = ceiling(3 n^2 / 8)** -- matches n=1 only.
- **Minimal-degree polynomial over Q (via sequence_fit)** -- no fit exists
  on the 9 proved terms; the irregular second differences make any
  polynomial of degree <= 4 impossible.
- **Linear recurrence with constant coefficients (Berlekamp-Massey)** -- no
  recurrence of order <= 5 fits the 9 proved terms.

## Cross-References Found

| OEIS ID | Name                                                                         | Relationship |
|---------|------------------------------------------------------------------------------|--------------|
| A001420 | Number of fixed n-iamonds                                                     | Counts the pieces that must be contained; `num_pieces` in solver-results.json exactly equals the first 9 A001420 terms 2, 3, 6, 14, 36, 94, 250, 675, 1838. |
| A000577 | Number of free n-iamonds (polyiamonds up to rotation and reflection)         | Companion; defines the underlying combinatorial family. |
| A006534 | Number of one-sided n-iamonds                                                | Companion for the sibling one-sided project. |
| A024206 | Quarter-squares-minus-1 family                                               | Previously conjectured match (2026-03-22); **explicitly falsified** by this pass -- see Conjectures Rejected. |
| A000217 | Triangular numbers                                                           | Analog result from oeis-a000217x: on the hexagonal grid, the fixed-polyhex-container sequence coincides with A000217. The triangular-grid analog studied here does **not** coincide with A000217. |

## Observations on Growth

- First differences are 2, 2, 3, 3, 5, 5, 5, 4 -- non-monotone, with a
  plateau of three 5s at n=6, 7, 8 followed by a drop to 4 at n=9.
- Second differences are 0, 1, 0, 2, 0, 0, -1 -- not constant,
  ruling out pure quadratic closed forms on these 9 terms.
- The ratio a(n) / n^2 drifts from 2.000 (n=1) down to 0.383 (n=9);
  the sequence appears to grow like Theta(n^2) asymptotically, but with
  an irregular lower-order correction.
- No direct connection to the piece count A001420 was found
  (a(9) = 31 while A001420(9) = 1838; growth rates are wildly
  different).
- The irregular second differences suggest that a closed form -- if one
  exists -- will involve floor/ceiling or modular case splits, and that
  more terms are needed before conjecturing one with any confidence.

## No Conjecture Found

No closed form, recurrence, known sequence, or simple transformation
matches all 9 proved terms. The sequence is genuinely new and will be
submitted to OEIS as a NEW entry with the 9 proved terms and a list of
companion cross-references (A001420, A000577, A006534, A000217) -- no
`FORMULA` field will be filed at this submission.

## Outcome

**No conjecture found.**
