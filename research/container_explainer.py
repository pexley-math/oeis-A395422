"""Manim animation explaining the container problem for A395422.

Cycles through n = 1 .. 6. For each n, shows the optimal container
(a(n) cells in teal) and then highlights each of the A001420(n) fixed
n-iamonds in turn at its valid parity-preserving translation inside the
container. Every piece holds on screen for 2 seconds.

Run: manim -ql container_explainer.py ContainerExplainer

Rendered GIF + MP4 are copied to research/container-animation.{gif,mp4}.
"""

from manim import *
import json
import math
import os
import sys

# Add shared library to path (same pattern as A369366)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from figure_gen_utils.manim_grids import tri_vertices, make_tri, build_shape_colored
from figure_gen_utils.manim_patterns import bottom_text


# ---------------------------------------------------------------------------
# Pure-Python fixed-polyiamond enumerator (no private-lib dependency).
# Matches sat_utils.tilings.polyiamond.tri_neighbours:
#   (r + c) even -> (r-1, c); (r + c) odd -> (r+1, c).
# ---------------------------------------------------------------------------

def _neighbours(r, c):
    if (r + c) % 2 == 0:
        return [(r, c - 1), (r, c + 1), (r - 1, c)]
    return [(r, c - 1), (r, c + 1), (r + 1, c)]


def _parity_shift(cells):
    mr = min(r for r, _ in cells)
    mc = min(c for _, c in cells)
    if (mr + mc) % 2 == 0:
        dr, dc = -mr, -mc
    else:
        dr, dc = -mr, -mc + 1
    return frozenset((r + dr, c + dc) for r, c in cells)


def _enumerate_fixed(n):
    if n == 1:
        return [frozenset({(0, 0)}), frozenset({(0, 1)})]
    prev = _enumerate_fixed(n - 1)
    seen = set()
    out = []
    for p in prev:
        for cell in p:
            for nb in _neighbours(*cell):
                if nb in p:
                    continue
                grown = _parity_shift(p | {nb})
                if grown not in seen:
                    seen.add(grown)
                    out.append(grown)
    return out


def _find_placement(piece, container):
    piece = list(piece)
    container_set = set(container)
    p_rs = [r for r, _ in piece]
    p_cs = [c for _, c in piece]
    c_rs = [r for r, _ in container]
    c_cs = [c for _, c in container]
    for dr in range(min(c_rs) - min(p_rs), max(c_rs) - max(p_rs) + 1):
        for dc in range(min(c_cs) - min(p_cs), max(c_cs) - max(p_cs) + 1):
            if (dr + dc) % 2 != 0:
                continue
            t = {(r + dr, c + dc) for r, c in piece}
            if t.issubset(container_set):
                return t
    return None


# ---------------------------------------------------------------------------
# Scene
# ---------------------------------------------------------------------------

CONTAINER_COLOR = TEAL_C
PIECE_COLOR = RED

BOTTOM_TEXT_Y = -3.2
HOLD_SECONDS = 2.0                # 2 s per piece, per user spec

# Cell-size scale per n (so the drawing stays on-screen for bigger containers)
SCALE_FOR_N = {1: 2.2, 2: 1.8, 3: 1.6, 4: 1.0, 5: 0.9, 6: 0.75}


class ContainerExplainer(Scene):
    """What does a(n) measure, for A395422?"""

    def construct(self):
        # ===== TITLE =====
        title = Text("What does a(n) measure?", font_size=40, weight=BOLD)
        sub = Text("A395422: smallest polyiamond containing all fixed n-iamonds",
                   font_size=22, color=GREY_B, weight=BOLD)
        sub.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), FadeIn(sub))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(sub))

        # ===== LOAD SOLVER WITNESSES =====
        results_path = os.path.join(os.path.dirname(__file__), "solver-results.json")
        with open(results_path) as f:
            results = json.load(f)

        for n in range(1, 4):
            self.show_an(n, results)

        # ===== SLIDESHOW: a(4) through a(9) =====
        self.slideshow(list(range(4, 10)), results)

        # ===== FINAL =====
        f1 = Text("a(n) = smallest connected polyiamond", font_size=32, weight=BOLD)
        f2 = Text("containing every fixed n-iamond as a translated subset",
                  font_size=26, weight=BOLD)
        f3 = Text("a(1..9) = 2, 4, 6, 9, 12, 17, 22, 27, 31",
                  font_size=30, color=YELLOW, weight=BOLD)
        fg = VGroup(f1, f2, f3).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(Write(f1), Write(f2))
        self.wait(1)
        self.play(Write(f3))
        self.wait(3)

    def show_an(self, n, results):
        """Show the container for a(n) and cycle through all fixed n-iamonds."""
        a_n = results[str(n)]["value"]
        container_cells = [tuple(c) for c in results[str(n)]["cells"]]
        container_set = set(container_cells)

        pieces = _enumerate_fixed(n)

        # Compute placements once so we can order by spatial flow.
        placements = {}
        for p in pieces:
            pl = _find_placement(p, container_set)
            if pl is None:
                raise RuntimeError(
                    f"n={n} piece does not fit inside the solver witness")
            placements[p] = frozenset(pl)

        def _cent(cells):
            cs = list(cells)
            return (sum(r for r, _ in cs) / len(cs),
                    sum(c for _, c in cs) / len(cs))

        # "Snake walk" ordering: start with the top-leftmost placement, then
        # at each step pick the unvisited placement that shares the most
        # cells with the current one (so the red highlight slides rather
        # than teleports). Break ties by centroid distance.
        remaining = list(pieces)
        remaining.sort(key=lambda p: _cent(placements[p]))  # topmost first
        ordered = [remaining.pop(0)]
        while remaining:
            cur = placements[ordered[-1]]
            cur_c = _cent(cur)
            def _score(p, cur=cur, cur_c=cur_c):
                pl = placements[p]
                overlap = len(pl & cur)
                cp = _cent(pl)
                cd = (cp[0] - cur_c[0]) ** 2 + (cp[1] - cur_c[1]) ** 2
                return (-overlap, cd)
            remaining.sort(key=_score)
            ordered.append(remaining.pop(0))
        pieces = ordered

        s = SCALE_FOR_N.get(n, 0.7)

        header = Text(f"a({n}) = {a_n}", font_size=44, color=YELLOW, weight=BOLD)
        header.to_edge(UP, buff=0.5)

        # Draw container in teal
        orbit_map = {rc: 0 for rc in container_cells}
        group, tris = build_shape_colored(container_cells, orbit_map,
                                          [CONTAINER_COLOR], s)

        self.play(Write(header), *[FadeIn(t) for t in tris.values()])

        intro = bottom_text(
            f"{a_n}-cell container for every fixed {n}-iamond "
            f"(each {n}-iamond = {n} triangle{'s' if n > 1 else ''})",
            y=BOTTOM_TEXT_Y,
            font_size=22 if n <= 3 else 20)
        self.play(FadeIn(intro))
        self.wait(1.5)

        prev_caption = intro
        total = len(pieces)
        for i, piece in enumerate(pieces, 1):
            placed = placements[piece]

            # Re-colour: container teal, piece red
            new_color_idx = {rc: 0 for rc in container_cells}
            for rc in placed:
                new_color_idx[rc] = 1
            colors = [CONTAINER_COLOR, PIECE_COLOR]

            anims = []
            for rc, tri in tris.items():
                target = colors[new_color_idx[rc]]
                anims.append(tri.animate.set_fill(target, opacity=0.85))

            caption = bottom_text(
                f"Piece {i} of {total}: a {n}-triangle fixed {n}-iamond, "
                f"shown in red inside the {a_n}-triangle container",
                y=BOTTOM_TEXT_Y, color=GREEN,
                font_size=20 if n <= 3 else 18)
            self.play(*anims,
                      ReplacementTransform(prev_caption, caption),
                      run_time=0.4)
            self.wait(HOLD_SECONDS)
            prev_caption = caption

        final = bottom_text(
            f"All {total} fixed {n}-iamonds fit. a({n}) = {a_n}.",
            y=BOTTOM_TEXT_Y, color=YELLOW,
            font_size=24 if n <= 3 else 20)
        self.play(ReplacementTransform(prev_caption, final))
        self.wait(2)
        self.play(*[FadeOut(m) for m in [header, group, final]])

    def slideshow(self, ns, results):
        """Quick slideshow of the optimal containers for each n in `ns`.

        No piece highlighting -- just the overall container shape per n,
        with a short header + caption, held for ~3 s each. Designed to
        compress well in GIF (long static holds) and to summarise the
        higher-n shapes without dwelling on their many pieces.
        """
        intro = Text("Optimal containers for n = 4 .. 9",
                     font_size=34, weight=BOLD)
        sub = Text("(shapes only; piece counts A001420(n) grow fast)",
                   font_size=22, color=GREY_B, weight=BOLD)
        sub.next_to(intro, DOWN, buff=0.3)
        self.play(Write(intro), FadeIn(sub))
        self.wait(1.5)
        self.play(FadeOut(intro), FadeOut(sub))

        for n in ns:
            a_n = results[str(n)]["value"]
            container_cells = [tuple(c) for c in results[str(n)]["cells"]]
            num_pieces = results[str(n)].get("num_pieces", "?")

            s = SCALE_FOR_N.get(n, 0.55 if n >= 8 else 0.75)
            header = Text(f"a({n}) = {a_n}", font_size=42,
                          color=YELLOW, weight=BOLD)
            header.to_edge(UP, buff=0.5)

            orbit_map = {rc: 0 for rc in container_cells}
            group, tris = build_shape_colored(container_cells, orbit_map,
                                              [CONTAINER_COLOR], s)

            caption = bottom_text(
                f"{a_n}-triangle container for all {num_pieces} fixed {n}-iamonds",
                y=BOTTOM_TEXT_Y,
                font_size=22 if n <= 5 else 20)

            self.play(Write(header),
                      *[FadeIn(t) for t in tris.values()],
                      FadeIn(caption),
                      run_time=0.8)
            self.wait(3.0)
            self.play(FadeOut(header), FadeOut(group), FadeOut(caption),
                      run_time=0.4)
