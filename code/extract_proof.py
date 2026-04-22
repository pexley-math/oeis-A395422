"""Prose-trace driver for oeis-a395422.

Validates that the shared prose-trace pipeline generalises beyond
Lee-codes to the container-family ContainerSolverFramework projects.
Second consumer of plan ``twinkly-bubbling-stearns`` (Phase H).

Differences from lee-quasi-cross-3-2-13's driver:
- The SAT encoder lives in the shared framework
  (``sat_utils.frameworks.container``), not a project-local module,
  and has not yet been retrofitted with ``label_store``.  We
  therefore render the trace with ``GenericTemplate`` -- the
  shared-library fallback that speaks variable-N / clause-N.
  Full domain-fluent rendering is a follow-up (retrofit the
  framework + add ``ContainerTemplate``).
- CNF + DRAT already ship on disk under ``research/drat/`` (emitted
  by ``solve_fixed-polyiamond-container.py --emit-drat``).  We load
  them directly rather than re-solving.

Usage:
    python extract_proof.py [--n N]

The project's ``a(n)`` values are 2, 4, 6, 9, 12, 17, 22, 27, 31, 39
for n=1..10.  For each n, the UNSAT CNF lives at
``research/drat/n{n}_k{a(n)-1}.cnf`` with companion DRAT.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_PROJ = Path(__file__).resolve().parent.parent
_ROOT = _PROJ.parent.parent   # research-outputs/paper-project
sys.path.insert(0, str(_ROOT))

from figure_gen_utils.versioned_output import save_versioned  # noqa: E402
from sat_utils.cnf_tools import import_cnf  # noqa: E402
from sat_utils.proof_labels import LabelStore  # noqa: E402
from sat_utils.propagation_trace import propagate  # noqa: E402
from sat_utils.prose_trace import render_markdown, render_typst  # noqa: E402
from sat_utils.prose_trace_container import (  # noqa: E402
    ContainerTemplate,
    build_label_store,
    descriptor_from_context,
)
from sat_utils.unsat_core import extract_unsat_core  # noqa: E402


# a(n) table from research/conjecture-report.md (n=1..10, corrected
# 2026-04-11 after the polyform_enum n=1 triangular fix).
A_VALUES = {
    1: 2, 2: 4, 3: 6, 4: 9, 5: 12,
    6: 17, 7: 22, 8: 27, 9: 31, 10: 39,
}


def _drat_paths(n: int):
    """Return (cnf_path, drat_path) for the lower-bound UNSAT instance
    at ``k = a(n) - 1``."""
    a = A_VALUES[n]
    k_lower = a - 1
    drat_dir = _PROJ / "research" / "drat"
    cnf = drat_dir / f"n{n}_k{k_lower}.cnf"
    drat = drat_dir / f"n{n}_k{k_lower}.drat"
    return cnf, drat, k_lower


def _summarise(*, n, k_lower, n_clauses, n_vars, core_r, trace) -> str:
    lines = [
        "## Encoding summary",
        "",
        f"- n = {n} (target: smallest polyiamond containing every "
        f"fixed n-iamond by translation)",
        f"- target lower bound: a({n}) > {k_lower}  "
        f"(i.e., no {k_lower}-cell polyiamond covers every fixed n-iamond)",
        f"- SAT variables: {n_vars}",
        f"- total clauses: {n_clauses}",
        f"- renderer template: ``ContainerTemplate`` with "
        f"descriptor_from_context (shared library, no framework "
        f"retrofit required)",
        "",
        "### Unit-propagation trace stats",
        "",
        f"- is_unsat_by_up: {trace.is_unsat_by_up}",
        f"- propagation steps recorded: {len(trace.steps)}",
        f"- conflict: {'yes' if trace.conflict is not None else 'no'}",
        "",
        "### MUC extraction",
        "",
        f"- drat-trim verdict: {core_r.get('verdict', 'skipped')}",
        f"- core clauses: {core_r.get('n_core_clauses', 0)} "
        f"of {core_r.get('n_original_clauses', n_clauses)}",
    ]
    if core_r.get("n_original_clauses"):
        pct = 100.0 * core_r["n_core_clauses"] / core_r["n_original_clauses"]
        lines.append(f"- core fraction: {pct:.1f}%")
    lines += [
        "",
        "_Note: rendering uses the shared "
        "``sat_utils.prose_trace_container.ContainerTemplate``, "
        "constructed from a ``ContainerDescriptor`` derived from the "
        "project's own framework instance via "
        "``descriptor_from_context``.  No framework retrofit is "
        "required -- cell, piece, symmetry, and CEGAR clauses are "
        "recognised from literal shapes.  See "
        "``tools/cadical-support/README.md`` for the native cadical "
        "build required by the DRAT emission step._",
    ]
    return "\n".join(lines) + "\n"


def run_pipeline(n: int) -> dict:
    if n not in A_VALUES:
        raise SystemExit(
            f"no a(n) value known for n={n}; extend A_VALUES in "
            f"extract_proof.py"
        )
    cnf_path, drat_path, k_lower = _drat_paths(n)
    if not cnf_path.exists() or not drat_path.exists():
        raise SystemExit(
            f"missing CNF or DRAT for n={n} at {cnf_path.parent}.  "
            f"Run: python code/solve_fixed-polyiamond-container.py "
            f"--n {n} --emit-drat --drat-output-dir research/drat"
        )

    clauses, n_vars = import_cnf(str(cnf_path))
    trace = propagate(clauses)
    core_r = extract_unsat_core(cnf_path, drat_path)

    # Build a ContainerDescriptor from the project solver so the
    # renderer speaks cell/piece vocabulary rather than variable-N.
    # Import lazily because the solver module instantiates its
    # framework at import time.
    sys.path.insert(0, str(_PROJ / "code"))
    import importlib
    solver_mod = importlib.import_module("solve_fixed-polyiamond-container")
    desc = descriptor_from_context(solver_mod.solver, n, k=k_lower)
    desc = type(desc)(
        n=desc.n, rows=desc.rows, cols=desc.cols,
        geometry=desc.geometry, k_lower=k_lower,
        cell_of=desc.cell_of, piece_of=desc.piece_of,
        cardinality_aux_range=desc.cardinality_aux_range,
    )
    labels = build_label_store(desc)
    template = ContainerTemplate(desc)
    core = core_r.get("clause_ids") or None
    problem_id = f"fixed-polyiamond-container n={n}"

    body = render_markdown(
        trace, labels,
        problem_id=problem_id, core=core, template=template,
    )
    md = body + "\n" + _summarise(
        n=n, k_lower=k_lower,
        n_clauses=len(clauses), n_vars=n_vars,
        core_r=core_r, trace=trace,
    )
    out_md = _PROJ / "research" / "proof-trace.md"
    save_versioned(md, str(out_md))

    typ_body = render_typst(
        trace, labels,
        problem_id=problem_id, core=core, template=template,
    )
    out_typ = _PROJ / "research" / "proof-trace.typ"
    save_versioned(typ_body, str(out_typ))

    return {
        "n": n,
        "k_lower": k_lower,
        "n_clauses": len(clauses),
        "n_vars": n_vars,
        "n_steps": len(trace.steps),
        "is_unsat_by_up": trace.is_unsat_by_up,
        "core_verdict": core_r.get("verdict"),
        "core_clauses": core_r.get("n_core_clauses"),
        "out_md": str(out_md),
        "out_typ": str(out_typ),
    }


def _parse_args(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--n", type=int, default=3)
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)
    summary = run_pipeline(args.n)
    for k, v in summary.items():
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
