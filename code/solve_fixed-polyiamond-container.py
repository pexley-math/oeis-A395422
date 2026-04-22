"""
Smallest Polyiamond Containing All FIXED n-Iamonds

Computes the smallest connected polyiamond (edge-connected union of up and
down unit triangles) that contains every fixed n-iamond as a subregion via
translation only (no rotation, no reflection). Provisionally matches OEIS
A024206 with an offset of +1 for n=1..10 (re-verification pending post
the 2026-04-11 `use_shape` heuristic retirement).

Architecture: subclasses ``sat_utils.frameworks.ContainerSolverFramework``
to plug in the triangular-lattice parity-dependent neighbour function
(up-pointing triangles neighbour left/right/above, down-pointing neighbour
left/right/below). All other pipeline plumbing (SAT + CEGAR connectivity,
top-down search, CLI wrapper, versioned JSON output, logging) comes from
the framework.

Usage:
    python solve_fixed-polyiamond-container.py --n 1-5
    python solve_fixed-polyiamond-container.py --n 1-10 --per-term-timeout 1800

License: CC-BY-4.0
"""

import sys
from typing import Callable, List, Tuple

from polyform_enum import TRIANGLE, enumerate_fixed

from sat_utils.frameworks import (
    ContainerSolverFramework,
    default_bridge_candidates,
)
from sat_utils.tilings.polyiamond import container_search_bounds_fixed


# A001420 -- number of fixed 2D triangular-celled animals with n cells
# (fixed polyiamonds). Used by the banner ``extra_lines_fn`` to
# sanity-check the polyform_enum Cython backend is returning the right
# counts. Matches the archived 2026-03-22 solver-results.json counts.
FIXED_POLYIAMOND_COUNTS = {
    # A001420 (offset 1): the n=1 term is 2, not 1, because the
    # triangular lattice has two distinct fixed 1-iamonds (up-pointing
    # and down-pointing). Corrected 2026-04-11 against the OEIS
    # authoritative b-file.
    1: 2, 2: 3, 3: 6, 4: 14, 5: 36, 6: 94, 7: 250, 8: 675, 9: 1838, 10: 5053,
}


def _a001420_banner_lines():
    """Sanity-check lines emitted into the solver banner.

    Verifies the polyform_enum.enumerate_fixed backend returns the
    expected A001420 counts for n=1..10 (the range the benchmark set
    typically covers).
    """
    lines = ["  Fixed polyiamond counts (A001420):"]
    for test_n in range(1, 11):
        count = len(list(enumerate_fixed(test_n, TRIANGLE)))
        expected = FIXED_POLYIAMOND_COUNTS.get(test_n, "?")
        tag = "OK" if count == expected else f"MISMATCH expected {expected}"
        lines.append(f"    n={test_n}: {count} fixed {test_n}-iamonds  {tag}")
    return lines


class _TriContainerFramework(ContainerSolverFramework):
    """ContainerSolverFramework with triangular-lattice parity-dependent
    neighbour function.

    The shared framework's default ``_neighbors_for_geometry`` assumes
    4-adjacency for non-hex geometries; the triangular grid needs
    3-adjacency with (r+c) parity deciding whether a triangle neighbours
    above or below. This override is the single point of departure from
    the base framework.
    """

    def _neighbors_for_geometry(
        self, rows: int, cols: int,
    ) -> Callable[[Tuple[int, int]], List[Tuple[int, int]]]:
        def neighbors_fn(cell):
            r, c = cell
            # Up-pointing (r+c even): left, right, above
            # Down-pointing (r+c odd): left, right, below
            if (r + c) % 2 == 0:
                cands = ((r, c - 1), (r, c + 1), (r - 1, c))
            else:
                cands = ((r, c - 1), (r, c + 1), (r + 1, c))
            return [
                (nr, nc) for nr, nc in cands
                if 0 <= nr < rows and 0 <= nc < cols
            ]
        return neighbors_fn


solver = _TriContainerFramework(
    seq_id="A024206",
    description=(
        "Smallest polyiamond containing all FIXED n-iamonds "
        "(translation only; triangular grid)"
    ),
    method_label="SAT + CEGAR connectivity (CaDiCaL via PySAT)",
    software_label="solve_fixed-polyiamond-container.py via "
                   "ContainerSolverFramework (triangular)",
    geometry="triangular",
    piece_enumerator=lambda n: enumerate_fixed(n, TRIANGLE),
    piece_mode="fixed",
    # Legacy (2026-03-22) used an n x n bounding grid and the upper bound
    # a(n) <= n^2 (trivially valid: the n x n square box is a container).
    # The framework defaults are looser; keeping the legacy choice
    # preserves search ordering compatibility for term-by-term parity
    # against the archived results.
    # Phase 5: tighter upper bound helper (shared lib). Cap at n*n
    # (grid size) so the bound never exceeds the available cells for
    # small n where the helper's empirical formula would overshoot.
    # A001420(1) = 2 fix (2026-04-11): at n=1 the fixed polyiamond set
    # has TWO pieces (up + down triangles) and the minimum container
    # is a 2-cell rhombus, so the n=1 grid must be at least 1 x 2 (2
    # cells). We floor the grid dimension at 2 and the upper bound at
    # 2 for n=1 to accommodate this; for n >= 2 the n x n convention
    # and the container_search_bounds_fixed helper are unchanged.
    upper_bound=lambda n: max(
        2,
        min(container_search_bounds_fixed(n)[1], n * n),
    ),
    # A001420(1) = 2 fix: for n = 1 we need a grid that can hold a
    # 2-cell container (up + down triangle). A 1 x 2 rectangle works
    # and has exactly 2 cells, so the SAT search's sum = k constraint
    # is trivially tight at k = 2 = grid size. For n >= 2 the n x n
    # grid is unchanged.
    grid_shape_fn=lambda n: (1, 2) if n == 1 else (n, n),
    # Triangular symmetry breakers are disabled (the legacy solver ran
    # unbreakered; D6 breakers for the triangular lattice are not in the
    # shared symmetry module yet). CEGAR connectivity handles shape
    # constraints.
    solver_name="cadical153",  # measured faster than auto (cadical195) on this problem; re-A/B before touching
    use_symmetry=True,  # 2026-04-11: framework adds parity-screened D6 subset breakers
    bridge_candidates_fn=default_bridge_candidates,  # Phase 3: CEGAR bridge cuts
    incremental=True,  # Phase 4: one solver + ITotalizer across the k sweep
    use_lonely_cell_clauses=True,  # Phase 5: pre-encode no-lonely-cell constraints
    # use_shape_pruning=False is the framework default. Iteration 1
    # of /solver-iterate tested True: values unchanged on n=1..9 but
    # total wall time rose 18.6 s -> 19.5 s. DISCARDED. Memory still
    # flags this flag as unsafe for the FREE polyiamond sibling at
    # higher n; keep it OFF here for correctness and speed.
    extra_lines_fn=_a001420_banner_lines,
)


if __name__ == "__main__":
    sys.exit(solver.main())
