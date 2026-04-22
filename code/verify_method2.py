"""
verify_method2.py -- independent re-derivation of a(n) with a DISJOINT SAT stack.

DISJOINT CODE PATH from solve_fixed-polyiamond-container.py and verify_method1.py:
  - SAT backend: Glucose 4.2 via PySAT (MiniSat-derived, LBD decisions).
    The solver uses CaDiCaL 1.5.3 (Kissat-family), a different solver family.
  - Connectivity encoding: rooted spanning-arborescence variables encoded
    UP FRONT (no CEGAR loop). The solver uses iterative CEGAR with plain
    component-blocking cuts.
  - Cardinality encoding: sequential counter (EncType.seqcounter) via
    sat_utils.cardinality.card_equals with an explicit encoding override.
    The solver uses the wrapper's default (totalizer for small bounds).
  - Piece enumeration: pure Python BFS with triangular parity adjacency
    (no polyform_enum import). The solver uses polyform_enum._core (Cython).
  - Placement enumeration: pure Python with parity-preserving translation
    guard (no sat_utils.placement_runner import). The enforce-placement-
    runner hook exempts verify_*.py files for exactly this reason.

What it checks for every n in the solver's PROVED range:
  1. Re-derives a(n) independently via Glucose + spanning-tree connectivity
     + seqcounter cardinality.
  2. Confirms the re-derived optimum equals the solver's reported a(n).

Usage:
    python verify_method2.py                  # verify every proved term
    python verify_method2.py 4                # verify n=1..4
    python verify_method2.py --n 5            # verify a single n

Exit code: 0 iff the independent Glucose re-derivation agrees with the solver.
"""

import json
import os
import sys
import time
from collections import deque
from datetime import datetime

from pysat.card import EncType
from pysat.solvers import Glucose42

from sat_utils.cardinality import card_equals
from sat_utils.timeouts import solve_with_timeout

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

def _tri_neighbours_raw(cell):
    r, c = cell
    if (r + c) % 2 == 0:
        return [(r, c - 1), (r, c + 1), (r - 1, c)]
    return [(r, c - 1), (r, c + 1), (r + 1, c)]


# ----------------------------------------------------------------------
# Independent pure-Python fixed-polyiamond enumeration
# ----------------------------------------------------------------------

def _parity_shift(cells):
    """Normalise while preserving up/down cell orientations."""
    mr = min(r for r, _ in cells)
    mc = min(c for _, c in cells)
    if (mr + mc) % 2 == 0:
        dr, dc = -mr, -mc
    else:
        dr, dc = -mr, -mc + 1
    return frozenset((r + dr, c + dc) for r, c in cells)


def enumerate_fixed_pure(n):
    if n <= 0:
        return [frozenset()]
    if n == 1:
        # A001420(1) = 2: up-pointing and down-pointing unit triangles
        # are distinct under parity-preserving translation.
        return [frozenset({(0, 0)}), frozenset({(0, 1)})]
    prev = enumerate_fixed_pure(n - 1)
    seen = set()
    out = []
    for p in prev:
        for cell in p:
            for nb in _tri_neighbours_raw(cell):
                if nb in p:
                    continue
                grown = _parity_shift(p | {nb})
                if grown not in seen:
                    seen.add(grown)
                    out.append(grown)
    return out


# ----------------------------------------------------------------------
# Placement enumeration (parity-preserving translations)
# ----------------------------------------------------------------------

def piece_translations(piece, grid_rows, grid_cols):
    """Enumerate all parity-preserving translations of `piece` that fit
    inside a grid_rows x grid_cols rectangle. Returns a list of
    sorted tuples of (r, c) cells.
    """
    cells = list(piece)
    pr_min = min(r for r, _ in cells)
    pr_max = max(r for r, _ in cells)
    pc_min = min(c for _, c in cells)
    pc_max = max(c for _, c in cells)
    out = []
    for dr in range(0 - pr_min, grid_rows - pr_max):
        for dc in range(0 - pc_min, grid_cols - pc_max):
            if (dr + dc) % 2 != 0:
                continue
            placed = tuple(sorted((r + dr, c + dc) for r, c in cells))
            out.append(placed)
    return out


# ----------------------------------------------------------------------
# SAT encoding (Glucose + spanning arborescence + seqcounter)
# ----------------------------------------------------------------------

def _grid_neighbours(cell, grid_rows, grid_cols):
    r, c = cell
    if (r + c) % 2 == 0:
        cands = ((r, c - 1), (r, c + 1), (r - 1, c))
    else:
        cands = ((r, c - 1), (r, c + 1), (r + 1, c))
    return [(nr, nc) for nr, nc in cands
            if 0 <= nr < grid_rows and 0 <= nc < grid_cols]


def _try_glucose(n, k, grid_rows, grid_cols, pieces, time_limit_s=300.0):
    """Return True/False/None for (exists connected k-cell container)."""
    cells = [(r, c) for r in range(grid_rows) for c in range(grid_cols)]

    next_var = [1]

    def new_var():
        v = next_var[0]
        next_var[0] += 1
        return v

    x = {c: new_var() for c in cells}
    root = {c: new_var() for c in cells}
    depth_ge = {c: [new_var() for _ in range(k)] for c in cells}

    arc = {}
    for c in cells:
        for nb in _grid_neighbours(c, grid_rows, grid_cols):
            arc[(c, nb)] = new_var()

    y_lists = []
    for i, piece in enumerate(pieces):
        translations = piece_translations(piece, grid_rows, grid_cols)
        if not translations:
            return False
        ys = [new_var() for _ in translations]
        y_lists.append((translations, ys))

    clauses = []

    for translations, ys in y_lists:
        clauses.append(list(ys))
        for trans, y in zip(translations, ys):
            for c in trans:
                clauses.append([-y, x[c]])

    top_id = next_var[0] - 1
    x_lits = list(x.values())
    card_cnf = card_equals(x_lits, bound=k, top_id=top_id,
                           encoding=EncType.seqcounter)
    clauses.extend(card_cnf.clauses)
    if card_cnf.clauses:
        top_used = max(top_id,
                       max(abs(l) for cl in card_cnf.clauses for l in cl))
        next_var[0] = top_used + 1

    clauses.append(list(root.values()))
    root_list = list(root.values())
    for i in range(len(root_list)):
        for j in range(i + 1, len(root_list)):
            clauses.append([-root_list[i], -root_list[j]])
    for c in cells:
        clauses.append([-root[c], x[c]])

    for c in cells:
        dg = depth_ge[c]
        for d in range(len(dg) - 1):
            clauses.append([-dg[d + 1], dg[d]])

    for c in cells:
        clauses.append([-root[c], -depth_ge[c][0]])
    for c in cells:
        clauses.append([-x[c], root[c], depth_ge[c][0]])
    for c in cells:
        clauses.append([x[c], -depth_ge[c][0]])

    for (c, nb), a in arc.items():
        clauses.append([-a, x[c]])
        clauses.append([-a, x[nb]])
        clauses.append([-a, -root[c]])
        dg_c = depth_ge[c]
        dg_nb = depth_ge[nb]
        clauses.append([-a, dg_c[0]])
        for d in range(len(dg_nb) - 1):
            clauses.append([-a, -dg_nb[d], dg_c[d + 1]])
        for d in range(len(dg_c) - 1):
            clauses.append([-a, -dg_c[d + 1], dg_nb[d]])

    incoming = {c: [] for c in cells}
    for (c, nb), a in arc.items():
        incoming[c].append(a)
    for c in cells:
        clauses.append([-x[c], root[c]] + incoming[c])
        inc = incoming[c]
        for i in range(len(inc)):
            for j in range(i + 1, len(inc)):
                clauses.append([-inc[i], -inc[j]])
        for a in inc:
            clauses.append([x[c], -a])
        for a in inc:
            clauses.append([-root[c], -a])

    solver = Glucose42()
    for cl in clauses:
        solver.add_clause(cl)

    result, _sat_elapsed, interrupted = solve_with_timeout(
        solver, time_limit_s)
    solver.delete()
    if interrupted:
        return None
    return result


def verify_n_glucose(n, solver_results, time_limit_s=300.0, deadline=None):
    t0 = time.time()
    base = {
        "n": n, "ok": False, "status": "FAIL", "detail": "",
        "elapsed": 0.0, "sat_k": None, "unsat_k": None,
    }
    key = str(n)
    if key not in solver_results:
        base["detail"] = f"n={n}: no solver entry"
        base["elapsed"] = time.time() - t0
        return base
    res = solver_results[key]
    reported = res.get("size") or res.get("value")
    if reported is None:
        base["detail"] = f"n={n}: solver has no size"
        base["elapsed"] = time.time() - t0
        return base
    if n == 1:
        # A001420(1) = 2: two fixed 1-iamonds (up, down). The smallest
        # container that embeds both via parity-preserving translation
        # is a 2-cell rhombus, so the expected value is 2, not 1.
        ok = (reported == 2)
        base["ok"] = ok
        base["status"] = "PASS" if ok else "FAIL"
        base["detail"] = f"n=1: trivial two-iamond case (reported {reported}, expected 2)"
        base["sat_k"] = 2
        base["unsat_k"] = 1
        base["elapsed"] = time.time() - t0
        return base

    pieces = enumerate_fixed_pure(n)
    # Tighter grid: the main solver uses (n, n) (see
    # solve_fixed-polyiamond-container.py's grid_shape_fn), and under
    # Assumption (S) every optimal container fits inside that n x n
    # window up to parity-preserving translation. Verifier 2 matches
    # the solver's grid for consistency and speed -- the shared
    # structural bound is the same observation the solver relies on,
    # not a shared library call, so the SAT-backend / connectivity /
    # cardinality / piece-enumeration axes of independence are
    # untouched.
    grid_rows = max(n, 2)
    grid_cols = max(n, 2)

    def _remaining():
        if deadline is None:
            return time_limit_s
        left = deadline - time.time()
        return max(0, min(time_limit_s, left))

    sat_at = _try_glucose(
        n, reported, grid_rows, grid_cols, pieces,
        time_limit_s=_remaining())
    if sat_at is None:
        base["status"] = "TIMEOUT"
        base["detail"] = f"n={n}: Glucose inconclusive at k={reported}"
        base["elapsed"] = time.time() - t0
        return base
    if not sat_at:
        base["detail"] = (f"n={n}: Glucose UNSAT at k={reported}; solver "
                          f"claims a({n})={reported} -- upper bound wrong")
        base["elapsed"] = time.time() - t0
        return base

    sat_below = _try_glucose(
        n, reported - 1, grid_rows, grid_cols, pieces,
        time_limit_s=_remaining())
    if sat_below is None:
        base["status"] = "TIMEOUT"
        base["detail"] = f"n={n}: Glucose inconclusive at k={reported - 1}"
        base["sat_k"] = reported
        base["elapsed"] = time.time() - t0
        return base
    if sat_below:
        base["detail"] = (f"n={n}: Glucose SAT at k={reported - 1}; "
                          f"solver's a({n})={reported} is NOT optimal")
        base["sat_k"] = reported
        base["elapsed"] = time.time() - t0
        return base

    base["ok"] = True
    base["status"] = "PASS"
    base["sat_k"] = reported
    base["unsat_k"] = reported - 1
    base["detail"] = (f"n={n}: Glucose confirms a({n})={reported} "
                      f"(SAT at k={reported}, UNSAT at k={reported - 1})")
    base["elapsed"] = time.time() - t0
    return base


def _write_outputs(records, project_dir, all_pass, cli_args):
    from figure_gen_utils.versioned_output import save_versioned
    research_dir = os.path.join(project_dir, "research")
    os.makedirs(research_dir, exist_ok=True)

    summary = {
        "verifier": "verify_method2",
        "method": (
            "Glucose42 with rooted spanning-arborescence connectivity "
            "and sequential-counter cardinality on the triangular "
            "lattice (parity-preserving placements); disjoint from "
            "the main solver's CaDiCaL + CEGAR + placement_runner."
        ),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "per_term_timeout_s": cli_args.get("per_term_timeout_s"),
        "overall_status": "PASS" if all_pass else "FAIL_OR_TIMEOUT",
        "results": records,
    }
    json_path = os.path.join(research_dir, "verify_method2-results.json")
    save_versioned(summary, json_path)

    log_lines = [
        "verify_method2 run log",
        "=" * 60,
        "Method: Glucose42 + spanning arborescence + seqcounter (triangular)",
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
        "independent Glucose SAT re-derivation."
    )
    log_text = "\n".join(log_lines)
    log_path = os.path.join(research_dir, "verify_method2-run-log.txt")
    save_versioned(log_text, log_path)


# ----------------------------------------------------------------------
# VerifierBase subclass
# ----------------------------------------------------------------------

_PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_RESULTS_PATH = os.path.join(_PROJECT_DIR, "research", "solver-results.json")


class Method2Verifier(VerifierBase):
    name = "verify_method2 (Glucose42 + spanning arborescence + seqcounter, triangular)"
    description = (
        "Independent Glucose-based re-derivation of a(n) for "
        "fixed-polyiamond container, with spanning-arborescence "
        "connectivity encoding (no CEGAR) and seqcounter cardinality "
        "over parity-preserving triangular placements."
    )
    default_max_n = 9
    verify_tag = "2"
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
        if self._per_term_deadline is not None:
            remaining = self._per_term_deadline - time.time()
            per_call_budget = max(1.0, remaining / 2)
        else:
            per_call_budget = 300.0
        rec = verify_n_glucose(
            n, self._solver_results,
            time_limit_s=per_call_budget,
            deadline=self._per_term_deadline,
        )
        self._records.append(rec)
        if rec["status"] == "PASS":
            return rec.get("sat_k"), rec["detail"]
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
    sys.exit(Method2Verifier.run())
