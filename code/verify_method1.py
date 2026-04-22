"""
verify_method1.py -- independent geometric verifier for fixed-polyiamond-container.

DISJOINT CODE PATH from solve_fixed-polyiamond-container.py:
  - Piece enumeration: pure-Python BFS over triangular axial coordinates
    with the (r + c)-parity up/down rule.  Does NOT import polyform_enum.
  - Containment check: direct set-inclusion over translated piece cells
    with parity-preserving (dr + dc even) translations.  Does NOT use
    any SAT backend.
  - No imports from solve_*.py.

What it verifies: given the solver's reported a(n) and container cells
for each n, confirm that (i) the container is edge-connected under the
triangular lattice adjacency, and (ii) every fixed n-iamond (enumerated
independently) fits inside the container by parity-preserving
translation only.

Outputs (independent audit trail, per the two-verifier rule):
  research/verify_method1-results.json   (per-n pass/fail + timing)
  research/verify_method1-run-log.txt    (verbose stdout transcript)

Usage:
    python verify_method1.py                              # all proved terms
    python verify_method1.py 7                             # verify n=1..7
    python verify_method1.py --n 3                         # single n
    python verify_method1.py --per-term-timeout 3600       # 1h per term
    python verify_method1.py --no-timeout                  # disable cap

Exit code: 0 iff all checks pass within budget.
"""

import json
import os
import sys
import time
from collections import deque
from datetime import datetime

_SHARED = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", ".."))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)
try:
    from figure_gen_utils.pipeline_timeouts import VERIFIER_TIMEOUT_S
except ImportError:
    VERIFIER_TIMEOUT_S = 3600
from sat_utils.verifier_base import VerifierBase


# ----------------------------------------------------------------------
# Triangular lattice adjacency (parity-dependent 3-neighbours)
# ----------------------------------------------------------------------

def _tri_neighbours(cell):
    r, c = cell
    if (r + c) % 2 == 0:
        # up-triangle: left, right, above
        return [(r, c - 1), (r, c + 1), (r - 1, c)]
    # down-triangle: left, right, below
    return [(r, c - 1), (r, c + 1), (r + 1, c)]


# ----------------------------------------------------------------------
# Independent pure-Python fixed-polyiamond enumerator
# ----------------------------------------------------------------------

def _parity_shift(cells):
    """Translate a cell set so its row-minimum is 0 and its column-minimum
    is either 0 (if the row-min cell has even parity) or 1 (if odd). This
    gives a canonical form that *preserves* the up/down parity pattern
    of every cell, so two fixed polyiamonds that differ only by cell
    orientations are kept distinct. This is the crux of the 2026-04-06
    parity bug fix: naive min-based normalisation flips the pattern and
    merges distinct fixed polyiamonds.
    """
    mr = min(r for r, _ in cells)
    mc = min(c for _, c in cells)
    # Preserve parity of the (mr, mc) origin.
    if (mr + mc) % 2 == 0:
        dr, dc = -mr, -mc
    else:
        dr, dc = -mr, -mc + 1
    return frozenset((r + dr, c + dc) for r, c in cells)


def enumerate_fixed_pure(n):
    """Enumerate all fixed n-cell polyiamonds via Python BFS growth.

    Fixed = distinct up to parity-preserving translation only. No
    rotation, no reflection. Independent of polyform_enum.

    A001420(1) = 2: on the triangular lattice the unit cell has two
    geometric orientations, and pure translation never maps an
    up-pointing triangle to a down-pointing one, so both orientations
    are distinct fixed 1-iamonds.
    """
    if n <= 0:
        return [frozenset()]
    if n == 1:
        return [frozenset({(0, 0)}), frozenset({(0, 1)})]
    prev = enumerate_fixed_pure(n - 1)
    seen = set()
    out = []
    for p in prev:
        for cell in p:
            for nb in _tri_neighbours(cell):
                if nb in p:
                    continue
                grown = _parity_shift(p | {nb})
                if grown not in seen:
                    seen.add(grown)
                    out.append(grown)
    return out


# ----------------------------------------------------------------------
# Connectivity and containment (both triangular-parity-aware)
# ----------------------------------------------------------------------

def _is_connected(cells):
    cs = set(cells)
    if len(cs) <= 1:
        return True
    start = next(iter(cs))
    seen = {start}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        for nb in _tri_neighbours(cell):
            if nb in cs and nb not in seen:
                seen.add(nb)
                queue.append(nb)
    return len(seen) == len(cs)


def _piece_fits(piece, container):
    """Does piece fit inside container via parity-preserving translation?

    piece: iterable of (r, c) cells with absolute positions (not
    normalised). Every translation (dr, dc) must satisfy (dr + dc) % 2
    == 0 so cell orientations are preserved.
    """
    cells = list(piece)
    if not cells:
        return True
    pr_min = min(r for r, _ in cells)
    pr_max = max(r for r, _ in cells)
    pc_min = min(c for _, c in cells)
    pc_max = max(c for _, c in cells)
    cr_min = min(r for r, _ in container)
    cr_max = max(r for r, _ in container)
    cc_min = min(c for _, c in container)
    cc_max = max(c for _, c in container)
    for dr in range(cr_min - pr_min, cr_max - pr_max + 1):
        for dc in range(cc_min - pc_min, cc_max - pc_max + 1):
            if (dr + dc) % 2 != 0:
                continue
            placed = {(r + dr, c + dc) for r, c in cells}
            if placed.issubset(container):
                return True
    return False


# ----------------------------------------------------------------------
# Per-n verification driver
# ----------------------------------------------------------------------

def verify_n(n, solver_results, deadline=None):
    t0 = time.time()
    base = {
        "n": n, "ok": False, "status": "FAIL", "detail": "",
        "elapsed": 0.0, "pieces_checked": 0, "container_size": 0,
    }
    key = str(n)
    if key not in solver_results:
        base["detail"] = f"n={n}: no entry in solver-results.json"
        base["elapsed"] = time.time() - t0
        return base
    res = solver_results[key]
    if res.get("status") != "PROVED":
        base["detail"] = f"n={n}: solver status is {res.get('status')}, not PROVED"
        base["elapsed"] = time.time() - t0
        return base

    cells_list = res.get("cells") or []
    container = {(c[0], c[1]) for c in cells_list}
    reported = res.get("size") or res.get("value")
    base["container_size"] = len(container)
    if len(container) != reported:
        base["detail"] = (
            f"n={n}: reported size {reported} != cell count {len(container)}"
        )
        base["elapsed"] = time.time() - t0
        return base

    if not _is_connected(container):
        base["detail"] = f"n={n}: reported container is NOT connected"
        base["elapsed"] = time.time() - t0
        return base

    pieces = enumerate_fixed_pure(n)
    # A001420: authoritative OEIS values. n=1 is 2 (up + down
    # triangle), not 1 as polyform_enum historically returned.
    expected_count = {1: 2, 2: 3, 3: 6, 4: 14, 5: 36, 6: 94, 7: 250,
                      8: 675, 9: 1838, 10: 5053}.get(n)
    if expected_count is not None and len(pieces) != expected_count:
        base["detail"] = (
            f"n={n}: independent enum returned {len(pieces)} pieces, "
            f"expected {expected_count} (A001420)"
        )
        base["elapsed"] = time.time() - t0
        return base

    for idx, p in enumerate(pieces):
        if deadline is not None and time.time() >= deadline:
            base["status"] = "TIMEOUT"
            base["detail"] = (
                f"n={n}: timed out after checking {idx}/{len(pieces)} "
                f"pieces in {time.time() - t0:.1f}s"
            )
            base["pieces_checked"] = idx
            base["elapsed"] = time.time() - t0
            return base
        if not _piece_fits(p, container):
            base["detail"] = (
                f"n={n}: fixed piece #{idx} ({sorted(p)}) does not fit"
            )
            base["pieces_checked"] = idx
            base["elapsed"] = time.time() - t0
            return base

    base["ok"] = True
    base["status"] = "PASS"
    base["pieces_checked"] = len(pieces)
    base["detail"] = (
        f"n={n}: {len(container)} cells connected, all {len(pieces)} "
        f"fixed {n}-iamonds contained (method1 geometric)"
    )
    base["elapsed"] = time.time() - t0
    return base


def _write_outputs(records, project_dir, all_pass, cli_args):
    from figure_gen_utils.versioned_output import save_versioned
    research_dir = os.path.join(project_dir, "research")
    os.makedirs(research_dir, exist_ok=True)

    summary = {
        "verifier": "verify_method1",
        "method": (
            "geometric set-inclusion on triangular lattice "
            "(pure Python BFS, parity-preserving translations, "
            "disjoint enumeration)"
        ),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "per_term_timeout_s": cli_args.get("per_term_timeout_s"),
        "overall_status": "PASS" if all_pass else "FAIL_OR_TIMEOUT",
        "results": records,
    }
    json_path = os.path.join(research_dir, "verify_method1-results.json")
    save_versioned(summary, json_path)

    log_lines = [
        "verify_method1 run log",
        "=" * 60,
        "Method: triangular geometric set-inclusion (pure Python BFS)",
        f"Timestamp: {summary['timestamp']}",
        f"Per-term timeout: {cli_args.get('per_term_timeout_s')} s",
        f"Overall: {summary['overall_status']}",
        "",
    ]
    for r in records:
        log_lines.append(
            f"  [{r['status']}] {r['detail']}  [{r['elapsed']:.1f}s]"
        )
    log_lines.append("")
    log_lines.append(
        "NO pre-primed values. All values derived from scratch by "
        "independent pure-Python enumeration."
    )
    log_text = "\n".join(log_lines)
    log_path = os.path.join(research_dir, "verify_method1-run-log.txt")
    save_versioned(log_text, log_path)


# ----------------------------------------------------------------------
# VerifierBase subclass
# ----------------------------------------------------------------------

_PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_RESULTS_PATH = os.path.join(_PROJECT_DIR, "research", "solver-results.json")


class Method1Verifier(VerifierBase):
    name = "verify_method1 (triangular geometric, pure-Python, independent enum)"
    description = (
        "Independent geometric verifier for fixed-polyiamond container: "
        "pure-Python piece enumeration with parity-preserving "
        "translations, set-inclusion containment, and triangular BFS "
        "connectivity. Disjoint code path from the solver."
    )
    default_max_n = 9
    verify_tag = "1"
    default_per_term_timeout = float(VERIFIER_TIMEOUT_S)

    def __init__(self):
        if not os.path.exists(_RESULTS_PATH):
            raise FileNotFoundError(
                f"solver-results.json not found at {_RESULTS_PATH}; "
                f"run the solver first."
            )
        with open(_RESULTS_PATH, "r", encoding="utf-8") as f:
            self._solver_results = json.load(f)
        self._records = []

    @classmethod
    def select_ns(cls, args):
        if not os.path.exists(_RESULTS_PATH):
            return []
        with open(_RESULTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        proved = sorted(
            int(k) for k, v in data.items() if v.get("status") == "PROVED"
        )
        if args.n is not None:
            return [args.n] if args.n in proved else []
        return [n for n in proved if n <= args.max_n]

    def verify_n(self, n):
        rec = verify_n(
            n, self._solver_results, deadline=self._per_term_deadline
        )
        self._records.append(rec)
        if rec["status"] == "PASS":
            return rec.get("container_size"), rec["detail"]
        if rec["status"] == "TIMEOUT":
            return None, f"TIMEOUT: {rec['detail']}"
        return None, rec["detail"]

    def expected(self, n):
        key = str(n)
        if key not in self._solver_results:
            return None
        res = self._solver_results[key]
        return res.get("size") or res.get("value")

    def save_artifacts(self, summary, log_text):
        _write_outputs(
            self._records,
            _PROJECT_DIR,
            summary["all_ok"],
            cli_args={"per_term_timeout_s": summary["per_term_timeout_s"]},
        )


if __name__ == "__main__":
    sys.exit(Method1Verifier.run())
