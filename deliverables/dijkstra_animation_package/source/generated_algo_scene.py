from __future__ import annotations

import json
from pathlib import Path

from manim import *


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((ROOT / "docs" / "narration_manifest.json").read_text())
SEGMENTS = {item["id"]: item for item in MANIFEST["segments"]}

BG = "#0B1020"
BASE = "#A9B4C7"
EDGE = "#56637A"
TEXT = "#F4F7FB"
MUTED = "#8B98AE"
TENTATIVE = "#F6C85F"
FINALIZED = "#32C7A5"
CURRENT = "#FF8C42"
FOCUS = "#5DA9FF"
SUCCESS = "#6EEB83"
WARNING = "#FF6B6B"
PANEL = "#141C30"

NODE_POSITIONS = {
    "A": np.array([-5.35, 0.0, 0.0]),
    "B": np.array([-3.75, 1.45, 0.0]),
    "C": np.array([-3.75, -1.45, 0.0]),
    "D": np.array([-1.65, -0.55, 0.0]),
    "E": np.array([-1.65, 1.45, 0.0]),
    "F": np.array([0.55, 1.45, 0.0]),
}

EDGES = [
    ("A", "B", 4),
    ("A", "C", 2),
    ("B", "C", 1),
    ("B", "D", 5),
    ("B", "E", 7),
    ("C", "D", 8),
    ("D", "E", 2),
    ("D", "F", 6),
    ("E", "F", 3),
]

WEIGHT_OFFSETS = {
    frozenset(("A", "B")): UP * 0.20 + LEFT * 0.05,
    frozenset(("A", "C")): DOWN * 0.20 + LEFT * 0.05,
    frozenset(("B", "C")): LEFT * 0.22,
    frozenset(("B", "D")): DOWN * 0.22,
    frozenset(("B", "E")): UP * 0.22,
    frozenset(("C", "D")): DOWN * 0.22,
    frozenset(("D", "E")): RIGHT * 0.23,
    frozenset(("D", "F")): DOWN * 0.22,
    frozenset(("E", "F")): UP * 0.22,
}


class DijkstraSceneBase(Scene):
    def setup(self):
        self.camera.background_color = BG
        self.role_state = {}
        self.layout_state = {}
        self.beat_state = {}
        self.nodes = {}
        self.edges = {}
        self.weights = {}
        self.distances = {}
        self.distance_font_sizes = {}
        self.current_ring = None

    def title(self, text: str):
        mob = Text(text, font_size=34, weight=BOLD, color=TEXT).to_edge(UP, buff=0.22)
        self.add(mob)
        return mob

    def build_graph(self, scale=1.0, shift=ORIGIN, show_weights=True, subset=None):
        chosen = EDGES if subset is None else [e for e in EDGES if frozenset(e[:2]) in subset]
        edge_group = VGroup()
        weight_group = VGroup()
        node_group = VGroup()

        for a, b, weight in chosen:
            pa = NODE_POSITIONS[a] * scale + shift
            pb = NODE_POSITIONS[b] * scale + shift
            line = Line(pa, pb, color=EDGE, stroke_width=4)
            self.edges[frozenset((a, b))] = line
            edge_group.add(line)
            if show_weights:
                label = Text(str(weight), font_size=22, color=TEXT)
                label.move_to((pa + pb) / 2 + WEIGHT_OFFSETS[frozenset((a, b))] * scale)
                label.add_background_rectangle(color=BG, opacity=0.92, buff=0.05)
                self.weights[frozenset((a, b))] = label
                weight_group.add(label)

        visible_nodes = sorted({n for e in chosen for n in e[:2]})
        for name in visible_nodes:
            circle = Circle(radius=0.34 * scale, stroke_color=BASE, stroke_width=4, fill_color=BG, fill_opacity=1)
            circle.move_to(NODE_POSITIONS[name] * scale + shift)
            label = Text(name, font_size=max(18, int(28 * scale)), weight=BOLD, color=TEXT).move_to(circle)
            node = VGroup(circle, label)
            self.nodes[name] = node
            self.role_state[name] = "undiscovered"
            node_group.add(node)

        graph = VGroup(edge_group, weight_group, node_group)
        self.layout_state["graph"] = graph
        return graph

    def edge(self, a, b):
        return self.edges[frozenset((a, b))]

    def set_node_role(self, name, role, animate=True):
        palette = {
            "undiscovered": (BG, BASE),
            "tentative": ("#3A2F13", TENTATIVE),
            "finalized": ("#103C36", FINALIZED),
        }
        fill, stroke = palette[role]
        self.role_state[name] = role
        action = self.nodes[name][0].animate.set_fill(fill, opacity=1).set_stroke(stroke, width=5)
        if animate:
            self.play(action, run_time=0.45)
        else:
            self.nodes[name][0].set_fill(fill, opacity=1).set_stroke(stroke, width=5)

    def set_current(self, name=None, animate=True):
        if self.current_ring is not None:
            old = self.current_ring
            self.current_ring = None
            if animate:
                self.play(FadeOut(old), run_time=0.3)
            else:
                self.remove(old)
        if name is not None:
            ring = Circle(radius=self.nodes[name][0].radius + 0.12, color=CURRENT, stroke_width=5)
            ring.move_to(self.nodes[name])
            self.current_ring = ring
            if animate:
                self.play(Create(ring), run_time=0.35)
            else:
                self.add(ring)

    def add_distance_labels(self, values, font_size=21):
        for name, value in values.items():
            label = Text(str(value), font_size=font_size, color=TENTATIVE)
            label.next_to(self.nodes[name], DOWN, buff=0.12)
            label.add_background_rectangle(color=BG, opacity=0.9, buff=0.03)
            self.distances[name] = label
            self.distance_font_sizes[name] = font_size
            self.add(label)

    def update_distance(self, name, value, color=TENTATIVE):
        old = self.distances[name]
        new = Text(str(value), font_size=self.distance_font_sizes.get(name, 21), color=color)
        new.move_to(old)
        new.add_background_rectangle(color=BG, opacity=0.9, buff=0.03)
        self.play(ReplacementTransform(old, new), run_time=0.45)
        self.distances[name] = new

    def badge(self, text, node, direction):
        badge = Text(text, font_size=18, weight=BOLD, color=TEXT)
        badge.next_to(self.nodes[node], direction, buff=0.22)
        box = RoundedRectangle(corner_radius=0.12, width=badge.width + 0.25, height=badge.height + 0.16,
                               stroke_color=FOCUS, fill_color=PANEL, fill_opacity=0.95)
        box.move_to(badge)
        return VGroup(box, badge)

    def panel(self, title, width=4.3, height=1.35, center=np.array([3.9, 1.5, 0])):
        box = RoundedRectangle(corner_radius=0.18, width=width, height=height,
                               stroke_color="#33415E", fill_color=PANEL, fill_opacity=0.96)
        box.move_to(center)
        heading = Text(title, font_size=19, weight=BOLD, color=FOCUS)
        heading.next_to(box.get_top(), DOWN, buff=0.12)
        return VGroup(box, heading)

    def replace_text(self, old, text, font_size=21, color=TEXT):
        new = Text(text, font_size=font_size, color=color).move_to(old)
        self.play(ReplacementTransform(old, new), run_time=0.4)
        return new

    def narrate(self, beat_id):
        self.beat_state["current"] = beat_id
        segment = SEGMENTS[beat_id]
        self.add_sound(str(ROOT / segment["audio_file"]))
        self.wait(float(segment["duration_seconds"]) + 0.12)

    def highlight_edge(self, a, b, color=FOCUS, width=8):
        self.play(self.edge(a, b).animate.set_color(color).set_stroke(width=width), run_time=0.35)

    def reset_edge(self, a, b):
        self.play(self.edge(a, b).animate.set_color(EDGE).set_stroke(width=4), run_time=0.25)

    def fade_all(self):
        mobs = list(self.mobjects)
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.75)
        self.wait(0.15)


class DijkstraProblemGoal(DijkstraSceneBase):
    def construct(self):
        self.title("Dijkstra's Algorithm — Problem and Goal")
        graph = self.build_graph(scale=0.92, shift=DOWN * 0.15)
        self.play(FadeIn(graph), run_time=1.0)
        start = self.badge("Start", "A", LEFT)
        target = self.badge("Target", "F", RIGHT)
        self.play(FadeIn(start), FadeIn(target), run_time=0.6)
        self.narrate("beat-1-1")

        route1 = [("A", "B"), ("B", "D"), ("D", "F")]
        self.play(*[self.edge(a, b).animate.set_color(FOCUS).set_stroke(width=8) for a, b in route1], run_time=0.8)
        eq1 = Text("4 + 5 + 6 = 15", font_size=30, weight=BOLD, color=FOCUS).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(eq1), run_time=0.35)
        self.narrate("beat-1-2")

        self.play(*[self.edge(a, b).animate.set_color(EDGE).set_stroke(width=4) for a, b in route1], FadeOut(eq1), run_time=0.45)
        route2 = [("A", "C"), ("C", "B"), ("B", "E"), ("E", "F")]
        self.play(*[self.edge(a, b).animate.set_color(TENTATIVE).set_stroke(width=8) for a, b in route2], run_time=0.8)
        eq2 = Text("2 + 1 + 7 + 3 = 13", font_size=30, weight=BOLD, color=TENTATIVE).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(eq2), run_time=0.35)
        self.narrate("beat-1-3")

        prompt = Text("Find the minimum total weight", font_size=30, weight=BOLD, color=TEXT).to_edge(DOWN, buff=0.25)
        self.play(*[self.edge(a, b).animate.set_color(EDGE).set_stroke(width=4) for a, b in route2], ReplacementTransform(eq2, prompt), run_time=0.55)
        self.wait(0.8)
        self.fade_all()


class DijkstraCoreConcept(DijkstraSceneBase):
    def construct(self):
        self.title("Core Concept — Tentative and Finalized")
        graph = self.build_graph(scale=0.80, shift=LEFT * 0.75 + DOWN * 0.05)
        self.play(FadeIn(graph), run_time=0.8)
        self.add_distance_labels({n: "0" if n == "A" else "∞" for n in NODE_POSITIONS})
        legend = VGroup(
            Text("Tentative", font_size=19, color=TENTATIVE),
            Text("Finalized", font_size=19, color=FINALIZED),
            Text("Current outline", font_size=19, color=CURRENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.35, 1.25, 0])
        self.play(FadeIn(legend), run_time=0.5)
        self.narrate("beat-2-1")

        rule = Text("Choose the smallest unfinalized distance", font_size=23, color=TEXT)
        rule.move_to([3.85, -0.75, 0])
        a_ring = SurroundingRectangle(self.distances["A"], color=FOCUS, buff=0.09, corner_radius=0.08)
        self.play(FadeIn(rule), Create(a_ring), run_time=0.45)
        self.narrate("beat-2-2")

        self.set_node_role("A", "finalized")
        self.set_current("A")
        self.play(FadeOut(a_ring), run_time=0.25)
        self.narrate("beat-2-3")

        self.highlight_edge("A", "B")
        self.update_distance("B", 4)
        self.set_node_role("B", "tentative")
        self.narrate("beat-2-4")
        self.reset_edge("A", "B")

        self.highlight_edge("A", "C")
        self.update_distance("C", 2)
        self.set_node_role("C", "tentative")
        self.set_current(None)
        self.narrate("beat-2-5")
        self.reset_edge("A", "C")

        compare = VGroup(
            SurroundingRectangle(self.distances["B"], color=MUTED, buff=0.08),
            SurroundingRectangle(self.distances["C"], color=FOCUS, buff=0.08),
        )
        self.play(Create(compare), run_time=0.4)
        self.narrate("beat-2-6")

        cue = Text("All edge weights ≥ 0", font_size=24, weight=BOLD, color=SUCCESS).move_to([3.9, -1.55, 0])
        self.play(FadeIn(cue), run_time=0.35)
        self.set_node_role("C", "finalized")
        self.narrate("beat-2-7")
        self.fade_all()


class DijkstraStateStructures(DijkstraSceneBase):
    def construct(self):
        self.title("Dijkstra's State")
        graph = self.build_graph(scale=0.68, shift=LEFT * 1.15 + DOWN * 0.15)
        self.play(FadeIn(graph), run_time=0.7)
        self.add_distance_labels({n: "0" if n == "A" else "∞" for n in NODE_POSITIONS}, font_size=18)

        # Persistent Scene 3 state legend required by the approved design.
        # It occupies the clear band above the graph and does not overlap the
        # queue / predecessor panels on the right.
        legend_box = RoundedRectangle(
            corner_radius=0.16,
            width=5.65,
            height=0.95,
            stroke_color="#33415E",
            fill_color=PANEL,
            fill_opacity=0.96,
        ).move_to([-3.15, 2.05, 0])
        legend_title = Text("State legend", font_size=16, weight=BOLD, color=FOCUS)
        legend_title.next_to(legend_box.get_top(), DOWN, buff=0.09)

        def legend_item(label, fill, stroke, current=False):
            marker = Circle(radius=0.11, fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=3)
            symbol = VGroup(marker)
            if current:
                symbol.add(Circle(radius=0.16, stroke_color=CURRENT, stroke_width=3).move_to(marker))
            text = Text(label, font_size=15, color=TEXT)
            return VGroup(symbol, text).arrange(RIGHT, buff=0.09)

        legend_items = VGroup(
            legend_item("Undiscovered", BG, BASE),
            legend_item("Tentative", "#3A2F13", TENTATIVE),
            legend_item("Finalized", "#103C36", FINALIZED),
            legend_item("Current", "#103C36", FINALIZED, current=True),
        ).arrange(RIGHT, buff=0.22)
        legend_items.next_to(legend_title, DOWN, buff=0.12)
        legend = VGroup(legend_box, legend_title, legend_items)

        queue_panel = self.panel("Min-priority queue", center=np.array([4.15, 1.55, 0]), height=1.35)
        prev_panel = self.panel("Previous", center=np.array([4.15, -0.05, 0]), height=1.35)
        rules = VGroup(
            Text("distance[A] = 0", font_size=18, color=TEXT),
            Text("others = ∞", font_size=18, color=TEXT),
            Text("previous = —", font_size=18, color=TEXT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([4.15, -1.75, 0])
        queue_text = Text("MIN →  (A, 0)", font_size=23, color=TENTATIVE).move_to(queue_panel[0]).shift(DOWN * 0.12)
        prev_text = Text("A:—  B:—  C:—  D:—  E:—  F:—", font_size=17, color=TEXT).move_to(prev_panel[0]).shift(DOWN * 0.12)
        self.play(FadeIn(legend), FadeIn(queue_panel), FadeIn(prev_panel), FadeIn(rules), FadeIn(queue_text), FadeIn(prev_text), run_time=0.6)
        self.narrate("beat-3-1")

        self.set_node_role("A", "finalized")
        self.set_current("A")
        queue_text = self.replace_text(queue_text, "MIN →  empty", font_size=23, color=MUTED)
        self.narrate("beat-3-2")

        self.highlight_edge("A", "B")
        self.update_distance("B", 4)
        self.set_node_role("B", "tentative")
        prev_text = self.replace_text(prev_text, "B←A", font_size=22)
        queue_text = self.replace_text(queue_text, "MIN →  (B, 4)", font_size=23, color=TENTATIVE)
        self.narrate("beat-3-3")
        self.reset_edge("A", "B")

        self.highlight_edge("A", "C")
        self.update_distance("C", 2)
        self.set_node_role("C", "tentative")
        prev_text = self.replace_text(prev_text, "B←A     C←A", font_size=22)
        queue_text = self.replace_text(queue_text, "MIN →  (C, 2)   (B, 4)", font_size=21, color=TENTATIVE)
        self.set_current(None)
        self.narrate("beat-3-4")
        self.reset_edge("A", "C")

        queue_text = self.replace_text(queue_text, "MIN →  (B, 4)", font_size=23, color=TENTATIVE)
        self.set_node_role("C", "finalized")
        self.set_current("C")
        self.narrate("beat-3-5")

        preview = Text("tentative values may improve", font_size=19, color=FOCUS).move_to([4.15, -2.55, 0])
        self.play(FadeIn(preview), run_time=0.3)
        self.highlight_edge("C", "B")
        self.update_distance("B", 3)
        prev_text = self.replace_text(prev_text, "B←C     C←A", font_size=22)
        queue_text = self.replace_text(queue_text, "MIN →  (B, 3)", font_size=23, color=TENTATIVE)
        self.narrate("beat-3-6")
        self.fade_all()


class DijkstraRelaxation(DijkstraSceneBase):
    def construct(self):
        self.title("One Relaxation — C to B")
        subset = {frozenset(("A", "B")), frozenset(("A", "C")), frozenset(("B", "C"))}
        graph = self.build_graph(scale=1.05, shift=LEFT * 0.55 + DOWN * 0.15, subset=subset)
        self.play(FadeIn(graph), run_time=0.7)
        self.add_distance_labels({"A": 0, "B": 4, "C": 2}, font_size=24)
        self.set_node_role("A", "finalized", animate=False)
        self.set_node_role("C", "finalized", animate=False)
        self.set_node_role("B", "tentative", animate=False)
        self.set_current("C", animate=False)

        formula_panel = self.panel("Relaxation test", center=np.array([4.0, 1.25, 0]), height=1.75)
        formula = Text("dist[C] + w(C,B) < dist[B] ?", font_size=23, color=TEXT).move_to(formula_panel[0]).shift(DOWN * 0.12)
        prev_panel = self.panel("Previous", center=np.array([4.0, -0.65, 0]), height=1.1)
        prev = Text("B ← A", font_size=25, color=TEXT).move_to(prev_panel[0]).shift(DOWN * 0.10)
        queue_panel = self.panel("Min-priority queue", center=np.array([4.0, -2.05, 0]), height=1.15)
        queue = Text("MIN →  (B, 4)   larger candidates", font_size=19, color=TENTATIVE).move_to(queue_panel[0]).shift(DOWN * 0.10)
        self.play(FadeIn(formula_panel), FadeIn(formula), FadeIn(prev_panel), FadeIn(prev), FadeIn(queue_panel), FadeIn(queue), run_time=0.6)
        self.narrate("beat-4-1")

        self.highlight_edge("C", "B")
        formula = self.replace_text(formula, "2 + 1 = 3", font_size=28, color=FOCUS)
        self.narrate("beat-4-2")

        formula = self.replace_text(formula, "3 < 4   TRUE", font_size=28, color=SUCCESS)
        self.play(self.edge("A", "B").animate.set_opacity(0.25), run_time=0.3)
        self.narrate("beat-4-3")

        self.update_distance("B", 3)
        self.narrate("beat-4-4")

        prev = self.replace_text(prev, "B ← C", font_size=25, color=SUCCESS)
        self.narrate("beat-4-5")

        queue = self.replace_text(queue, "MIN →  (B, 3)   larger candidates", font_size=19, color=TENTATIVE)
        summary = Text("shorter → update distance, previous, queue", font_size=22, weight=BOLD, color=SUCCESS).to_edge(DOWN, buff=0.22)
        self.play(FadeIn(summary), run_time=0.35)
        self.narrate("beat-4-6")
        self.fade_all()


class DijkstraFullRun(DijkstraSceneBase):
    def construct(self):
        self.title("Full Dijkstra Run — A to F")
        graph = self.build_graph(scale=0.66, shift=LEFT * 1.35 + DOWN * 0.20)
        self.play(FadeIn(graph), run_time=0.7)
        self.add_distance_labels({n: "0" if n == "A" else "∞" for n in NODE_POSITIONS}, font_size=18)
        start = self.badge("Start", "A", LEFT)
        target = self.badge("Target", "F", RIGHT)
        self.play(FadeIn(start), FadeIn(target), run_time=0.4)

        queue_panel = self.panel("Min-priority queue", center=np.array([4.15, 1.65, 0]), height=1.25)
        prev_panel = self.panel("Previous", center=np.array([4.15, 0.12, 0]), height=1.25)
        calc_panel = self.panel("Active check", center=np.array([4.15, -1.50, 0]), height=1.35)
        queue = Text("MIN → (A,0)", font_size=21, color=TENTATIVE).move_to(queue_panel[0]).shift(DOWN * 0.11)
        prev = Text("all —", font_size=20, color=MUTED).move_to(prev_panel[0]).shift(DOWN * 0.11)
        calc = Text("ready", font_size=20, color=MUTED).move_to(calc_panel[0]).shift(DOWN * 0.11)
        self.play(FadeIn(queue_panel), FadeIn(prev_panel), FadeIn(calc_panel), FadeIn(queue), FadeIn(prev), FadeIn(calc), run_time=0.6)
        self.narrate("beat-5-1")

        queue = self.replace_text(queue, "MIN → empty", font_size=21, color=MUTED)
        self.set_node_role("A", "finalized")
        self.set_current("A")
        self.narrate("beat-5-2")

        self.highlight_edge("A", "B")
        calc = self.replace_text(calc, "0 + 4 → B = 4", font_size=21, color=FOCUS)
        self.update_distance("B", 4)
        self.set_node_role("B", "tentative")
        prev = self.replace_text(prev, "B←A", font_size=21)
        queue = self.replace_text(queue, "MIN → (B,4)", font_size=21, color=TENTATIVE)
        self.narrate("beat-5-3")
        self.reset_edge("A", "B")

        self.highlight_edge("A", "C")
        calc = self.replace_text(calc, "0 + 2 → C = 2", font_size=21, color=FOCUS)
        self.update_distance("C", 2)
        self.set_node_role("C", "tentative")
        prev = self.replace_text(prev, "B←A   C←A", font_size=21)
        queue = self.replace_text(queue, "MIN → (C,2)  (B,4)", font_size=20, color=TENTATIVE)
        self.set_current(None)
        self.narrate("beat-5-4")
        self.reset_edge("A", "C")

        queue = self.replace_text(queue, "MIN → (B,4)", font_size=21, color=TENTATIVE)
        self.set_node_role("C", "finalized")
        self.set_current("C")
        calc = self.replace_text(calc, "extract (C,2)", font_size=21, color=FINALIZED)
        self.narrate("beat-5-5")

        self.highlight_edge("C", "A", color=MUTED, width=6)
        calc = self.replace_text(calc, "C—A: A already finalized", font_size=19, color=MUTED)
        self.narrate("beat-5-6")
        self.reset_edge("C", "A")

        self.highlight_edge("C", "B")
        calc = self.replace_text(calc, "2 + 1 < 4  →  B = 3", font_size=20, color=SUCCESS)
        self.update_distance("B", 3)
        prev = self.replace_text(prev, "B←C   C←A", font_size=21)
        queue = self.replace_text(queue, "MIN → (B,3)", font_size=21, color=TENTATIVE)
        self.narrate("beat-5-7")
        self.reset_edge("C", "B")

        self.highlight_edge("C", "D")
        calc = self.replace_text(calc, "2 + 8 → D = 10", font_size=20, color=FOCUS)
        self.update_distance("D", 10)
        self.set_node_role("D", "tentative")
        prev = self.replace_text(prev, "B←C   C←A   D←C", font_size=19)
        queue = self.replace_text(queue, "MIN → (B,3)  (D,10)", font_size=19, color=TENTATIVE)
        self.set_current(None)
        self.narrate("beat-5-8")
        self.reset_edge("C", "D")

        queue = self.replace_text(queue, "MIN → (D,10)", font_size=20, color=TENTATIVE)
        self.set_node_role("B", "finalized")
        self.set_current("B")
        calc = self.replace_text(calc, "extract (B,3)", font_size=21, color=FINALIZED)
        self.narrate("beat-5-9")

        self.highlight_edge("B", "D")
        calc = self.replace_text(calc, "3 + 5 < 10  →  D = 8", font_size=20, color=SUCCESS)
        self.update_distance("D", 8)
        prev = self.replace_text(prev, "B←C   C←A   D←B", font_size=19)
        queue = self.replace_text(queue, "MIN → (D,8)", font_size=20, color=TENTATIVE)
        self.narrate("beat-5-10")
        self.reset_edge("B", "D")

        self.highlight_edge("B", "E")
        calc = self.replace_text(calc, "3 + 7 → E = 10", font_size=20, color=FOCUS)
        self.update_distance("E", 10)
        self.set_node_role("E", "tentative")
        prev = self.replace_text(prev, "B←C  C←A  D←B  E←B", font_size=18)
        queue = self.replace_text(queue, "MIN → (D,8)  (E,10)", font_size=19, color=TENTATIVE)
        self.set_current(None)
        self.narrate("beat-5-11")
        self.reset_edge("B", "E")

        queue = self.replace_text(queue, "MIN → (E,10)", font_size=20, color=TENTATIVE)
        self.set_node_role("D", "finalized")
        self.set_current("D")
        calc = self.replace_text(calc, "extract (D,8)", font_size=21, color=FINALIZED)
        self.narrate("beat-5-12")

        self.highlight_edge("D", "E", color=WARNING, width=7)
        calc = self.replace_text(calc, "8 + 2 = 10   not < 10", font_size=20, color=WARNING)
        self.narrate("beat-5-13")
        self.reset_edge("D", "E")

        self.highlight_edge("D", "F")
        calc = self.replace_text(calc, "8 + 6 → F = 14", font_size=20, color=FOCUS)
        self.update_distance("F", 14)
        self.set_node_role("F", "tentative")
        prev = self.replace_text(prev, "B←C  C←A  D←B  E←B  F←D", font_size=17)
        queue = self.replace_text(queue, "MIN → (E,10)  (F,14)", font_size=19, color=TENTATIVE)
        self.set_current(None)
        not_done = Text("Target discovered — not finalized", font_size=18, color=WARNING).to_edge(DOWN, buff=0.18)
        self.play(FadeIn(not_done), run_time=0.3)
        self.narrate("beat-5-14")
        self.reset_edge("D", "F")

        queue = self.replace_text(queue, "MIN → (F,14)", font_size=20, color=TENTATIVE)
        self.set_node_role("E", "finalized")
        self.set_current("E")
        calc = self.replace_text(calc, "extract (E,10)", font_size=21, color=FINALIZED)
        self.play(FadeOut(not_done), run_time=0.25)
        self.narrate("beat-5-15")

        self.highlight_edge("E", "F")
        calc = self.replace_text(calc, "10 + 3 < 14  →  F = 13", font_size=20, color=SUCCESS)
        self.update_distance("F", 13)
        prev = self.replace_text(prev, "B←C  C←A  D←B  E←B  F←E", font_size=17)
        queue = self.replace_text(queue, "MIN → (F,13)", font_size=20, color=TENTATIVE)
        self.set_current(None)
        self.narrate("beat-5-16")
        self.reset_edge("E", "F")

        queue = self.replace_text(queue, "MIN → empty", font_size=21, color=MUTED)
        self.set_node_role("F", "finalized")
        self.set_current("F")
        calc = self.replace_text(calc, "extract (F,13)  →  STOP", font_size=21, color=SUCCESS)
        stop = Text("Target finalized: shortest distance = 13", font_size=21, weight=BOLD, color=SUCCESS).to_edge(DOWN, buff=0.18)
        self.play(FadeIn(stop), run_time=0.3)
        self.narrate("beat-5-17")
        self.set_current(None)
        self.play(FadeOut(queue_panel), FadeOut(queue), FadeOut(calc_panel), FadeOut(calc), run_time=0.45)
        self.wait(0.6)
        self.fade_all()


class DijkstraResultRecap(DijkstraSceneBase):
    def construct(self):
        self.title("Shortest Path and Recap")
        graph = self.build_graph(scale=0.78, shift=LEFT * 0.9 + DOWN * 0.10)
        self.play(FadeIn(graph), run_time=0.7)
        final_dist = {"A": 0, "B": 3, "C": 2, "D": 8, "E": 10, "F": 13}
        self.add_distance_labels(final_dist, font_size=20)
        for n in NODE_POSITIONS:
            self.set_node_role(n, "finalized", animate=False)
        result = Text("Shortest distance: 13", font_size=27, weight=BOLD, color=SUCCESS).move_to([4.05, 1.75, 0])
        prev = Text("F←E←B←C←A", font_size=26, color=TEXT).move_to([4.05, 0.95, 0])
        self.play(FadeIn(result), FadeIn(prev), run_time=0.5)
        self.narrate("beat-6-1")

        backward = [("E", "F"), ("B", "E"), ("C", "B"), ("A", "C")]
        for a, b in backward:
            self.play(self.edge(a, b).animate.set_color(FOCUS).set_stroke(width=8), run_time=0.32)
        self.narrate("beat-6-2")

        path_text = Text("A → C → B → E → F", font_size=25, weight=BOLD, color=TENTATIVE).move_to(prev)
        self.play(ReplacementTransform(prev, path_text), run_time=0.45)
        route_keys = {frozenset(e) for e in [("A", "C"), ("C", "B"), ("B", "E"), ("E", "F")]}
        self.play(*[line.animate.set_opacity(1 if key in route_keys else 0.18) for key, line in self.edges.items()], run_time=0.5)
        total = Text("2 + 1 + 7 + 3 = 13", font_size=25, color=SUCCESS).move_to([4.05, 0.15, 0])
        self.play(FadeIn(total), run_time=0.35)
        self.narrate("beat-6-3")

        recap = VGroup(
            Text("Extract minimum", font_size=21, color=FOCUS),
            Text("Finalize distance", font_size=21, color=FINALIZED),
            Text("Relax edges", font_size=21, color=TENTATIVE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.05, -1.35, 0])
        for item in recap:
            self.play(FadeIn(item, shift=RIGHT * 0.12), run_time=0.3)
        self.narrate("beat-6-4")

        condition = Text("Requires non-negative edge weights", font_size=20, weight=BOLD, color=TEXT).to_edge(DOWN, buff=0.18)
        self.play(FadeIn(condition), run_time=0.35)
        self.narrate("beat-6-5")
        self.wait(0.8)
        self.fade_all()
