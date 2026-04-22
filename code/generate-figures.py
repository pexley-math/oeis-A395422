"""
Generate publication figures and personal understanding diagram for
oeis-a395422 (fixed-polyiamond container problem).

Reads research/solver-results.json and produces:
- submission/fixed-polyiamond-container-figures.typ (+ .pdf)
- research/fixed-polyiamond-container-understanding.typ (+ .pdf)

Single-state binary rendering: every cell of the optimal container is
filled uniformly in teal. The understanding diagram annotates the
n = 10 container (a_"box"(10) = 39) with plain-text labels explaining
what the number means, the parity/orientation structure of the
triangular lattice, and the conditional nature of the bound via
Assumption (S).

Usage:
    python code/generate-figures.py
"""

import json
import sys
from pathlib import Path

PROJ_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJ_ROOT))

from figure_gen_utils.document_builder import DocumentBuilder
from figure_gen_utils.grid_triangle import triangle_figure_typst
from figure_gen_utils.typst_page import compile_typst

PROJ_DIR = Path(__file__).resolve().parent.parent

CONTAINER_COLOR = "#1ABC9C"   # teal -- the optimal container


def load_results():
    path = PROJ_DIR / "research" / "solver-results.json"
    return json.loads(path.read_text())


def generate_publication_figures(results):
    ns = sorted(int(k) for k in results)
    seq_str = ", ".join(str(results[str(n)]["value"]) for n in ns)

    doc = DocumentBuilder(
        title="Smallest Connected Polyiamond Containing All Fixed n-Iamonds",
        description=(
            '$a_"box"(n)$ = minimum number of triangular cells in a '
            'connected polyiamond, whose cells lie inside an '
            '$n times n$ rectangle (or $1 times 2$ for $n = 1$) up to '
            'parity-preserving translation, that contains every fixed '
            '$n$-iamond as a translated subset. Rotations and reflections '
            'are distinct.'),
        sequence_line=f'$a_"box"(1..{len(ns)}) = {seq_str}$',
    )

    for n in ns:
        entry = results[str(n)]
        a_n = entry["value"]
        cells = [tuple(c) for c in entry["cells"]]
        bbox = entry.get("bbox", "?")
        pieces = entry.get("num_pieces", "?")
        elapsed_raw = entry.get("elapsed", "?")
        if isinstance(elapsed_raw, (int, float)):
            elapsed = f"{elapsed_raw:.1f}"
        else:
            elapsed = str(elapsed_raw)
        detail_text = (
            f"{a_n} cells, {pieces} fixed $n$-iamonds, "
            f"bbox {bbox}, solved in {elapsed}s within the search rectangle"
        )
        doc.add_triangle_figure(
            cells=cells,
            n=n,
            k=a_n,
            status="PROVED",
            method="SAT + CEGAR",
            fill_color=CONTAINER_COLOR,
            detail_text=detail_text,
        )

    out_typ = PROJ_DIR / "submission" / "fixed-polyiamond-container-figures.typ"
    out_typ.parent.mkdir(parents=True, exist_ok=True)
    doc.generate(str(out_typ))
    print(f"Generated: {out_typ}")

    out_pdf = PROJ_DIR / "submission" / "fixed-polyiamond-container-figures.pdf"
    try:
        doc.compile(pdf_path=str(out_pdf))
        print(f"Compiled: {out_pdf}")
    except Exception as e:
        print(f"Typst compile failed for publication figures: {e}")
        print("  (.typ source saved; compile manually)")


def generate_understanding_figure(results):
    """Standalone explanatory diagram keyed to a_"box"(10) = 39.

    Shows the optimal 39-cell container for n = 10, annotated with plain
    text explaining what the value means and how it differs from the
    hex-grid analogue (A000217).
    """
    n = 10
    entry = results[str(n)]
    a_n = entry["value"]
    container = [tuple(c) for c in entry["cells"]]
    num_pieces = entry.get("num_pieces", "?")
    bbox = entry.get("bbox", "?")

    body, w_cm, h_cm = triangle_figure_typst(container, fill_color=CONTAINER_COLOR)

    parts = []
    parts.append('#set page(paper: "a4", margin: 1.5cm)')
    parts.append('#set text(font: "New Computer Modern", size: 10pt)')
    parts.append('')
    parts.append('#align(center)[')
    parts.append(f'  #text(size: 14pt, weight: "bold")'
                 f'[What does $a_"box"({n}) = {a_n}$ mean?]')
    parts.append('  #v(0.3em)')
    parts.append(f'  #text(size: 10pt)[This {a_n}-cell connected polyiamond '
                 f'contains every fixed {n}-cell polyiamond '
                 f'({num_pieces} shapes) as a translated subset]')
    parts.append(']')
    parts.append('#v(0.8em)')
    parts.append('#align(center)[')
    parts.append(body)
    parts.append(']')
    parts.append('#v(0.8em)')
    parts.append('#text(size: 10pt)[')
    parts.append(f'*The idea.* Every one of the {num_pieces} fixed '
                 f'{n}-cell polyiamonds (shapes where rotations and '
                 f'reflections are counted as distinct) can be placed, '
                 f'by parity-preserving translation alone, somewhere '
                 f'inside the teal region above. The bounding box of the '
                 f'container is {bbox}, which sits inside the solver search '
                 f'rectangle of ${n} times {n}$.')
    parts.append(']')
    parts.append('#v(0.5em)')
    parts.append('#text(size: 10pt)[')
    parts.append(f'*Orientation and parity.* The triangular lattice has '
                 f'two cell orientations: up-pointing and down-pointing. '
                 f'In our $(r, c)$ coordinates, a cell is up-pointing when '
                 f'$(r + c)$ is even and down-pointing when $(r + c)$ is '
                 f'odd. Pure translation (parity-preserving shift) never '
                 f'swaps orientations, so the up- and down-pointing '
                 f'monotriangles count as two distinct fixed 1-iamonds '
                 f'(matching OEIS A001420(1) = 2) -- and the count of '
                 f'fixed $n$-iamonds is $2, 3, 6, 14, 36, 94, 250, 675, '
                 f'1838, 5053$ for $n = 1$ through $10$.')
    parts.append(']')
    parts.append('#v(0.5em)')
    parts.append('#text(size: 10pt)[')
    parts.append(f'*How it was proved.* For each $n = 1, ..., 10$, '
                 f'a SAT solver with CEGAR connectivity search descended '
                 f'$k -> k - 1$ within the $n times n$ rectangle '
                 f'until it produced a model of size $a_"box"(n)$ and an '
                 f'UNSAT certificate at $a_"box"(n) - 1$. Every proved '
                 f'value is independently cross-checked by two verifiers '
                 f'with disjoint code paths from the main solver: a '
                 f'pure-Python geometric containment verifier and a '
                 f'Glucose-based spanning-arborescence re-optimiser. '
                 f'All three stacks agree on $n = 1..10$.')
    parts.append(']')
    parts.append('#v(0.5em)')
    parts.append('#text(size: 10pt)[')
    parts.append(f'*Conditional reading.* The proved value $a_"box"(n)$ is '
                 f'the minimum container size subject to the container '
                 f'cells fitting inside the $n times n$ rectangle '
                 f'after a parity-preserving translation. Assumption (S) '
                 f'in the paper states that at least one unrestricted '
                 f'minimum container fits inside such a rectangle for '
                 f'every $n$; under (S), $a_"box"(n) = a(n)$ for all '
                 f'$n >= 1$. Every computed optimal container in '
                 f'$n = 1..10$ is consistent with (S), but a general '
                 f'proof is open.')
    parts.append(']')
    parts.append('#v(0.5em)')
    parts.append('#text(size: 10pt)[')
    parts.append(f'*Contrast with the hexagonal grid.* On the hex grid '
                 f'(the sibling problem tracked in oeis-a000217x), the '
                 f'fixed-polyhex container sequence coincides with the '
                 f'triangular numbers $T_n = n(n + 1)/2$ through $n = 7$, '
                 f'giving a clean closed form. On the triangular lattice '
                 f'no such coincidence holds: $a_"box"(1..10) = 2, 4, 6, 9, '
                 f'12, 17, 22, 27, 31, 39$ does not match any simple '
                 f'closed form, linear recurrence, or known OEIS '
                 f'sequence -- including A024206, which was tentatively '
                 f'conjectured in a prior pass and is falsified '
                 f'term-by-term in the paper.')
    parts.append(']')

    content = "\n".join(parts)

    out_typ = PROJ_DIR / "research" / "fixed-polyiamond-container-understanding.typ"
    out_typ.parent.mkdir(parents=True, exist_ok=True)
    out_typ.write_text(content, encoding="utf-8")
    print(f"Generated: {out_typ}")

    out_pdf = PROJ_DIR / "research" / "fixed-polyiamond-container-understanding.pdf"
    try:
        compile_typst(str(out_typ), str(out_pdf))
        print(f"Compiled: {out_pdf}")
    except Exception as e:
        print(f"Typst compile failed for understanding figure: {e}")
        print("  (.typ source saved; compile manually)")


def main():
    results = load_results()
    generate_publication_figures(results)
    generate_understanding_figure(results)


if __name__ == "__main__":
    main()
