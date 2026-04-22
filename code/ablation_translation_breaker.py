"""Ablation runner: translation breaker on vs off on fixed-polyiamond
container, for n=1..N.

Thin wrapper over ``sat_utils.ablation.ablate_flag`` so the heavy
lifting lives in the shared library and every project can ablate its
own flags with a two-line script.

Run:
    python ablation_translation_breaker.py --upto 8
"""

from __future__ import annotations

import argparse
import importlib
import sys

from sat_utils.ablation import (
    ablate_flag,
    ablation_exit_code,
    format_ablation_table,
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--upto", type=int, default=8)
    ap.add_argument("--per-term-timeout", type=float, default=600.0)
    args = ap.parse_args()

    mod = importlib.import_module("solve_fixed-polyiamond-container")
    rows = ablate_flag(
        mod.solver,
        n_values=list(range(1, args.upto + 1)),
        flag_name="use_translation_breaker",
        per_term_timeout_s=args.per_term_timeout,
    )
    print(f"Ablation (n=1..{args.upto}), "
          f"per-term-timeout {args.per_term_timeout:.0f}s")
    print(format_ablation_table(
        rows, flag_name="use_translation_breaker",
    ))
    return ablation_exit_code(rows)


if __name__ == "__main__":
    sys.exit(main())
