from manim import *


class AlgorithmAnimation(Scene):
    FONT_SIZE = 30

    COLOR_DEFAULT = BLUE_D
    COLOR_CURRENT = YELLOW
    COLOR_FRONTIER = ORANGE
    COLOR_VISITED = GREEN_D

    def construct(self):
        state_trace = [
            {"action": "create_graph", "id": "g1", "nodes": ["A", "B", "C", "D", "E", "F"], "edges": [["A", "B"], ["A", "C"], ["B", "D"], ["B", "E"], ["C", "F"]]},
            {"action": "highlight_node", "target_id": "g1", "node_id": "A", "color": "YELLOW"},
            {"action": "mark_visited", "target_id": "g1", "node_id": "A", "color": "GREEN"},
            {"action": "highlight_node", "target_id": "g1", "node_id": "A", "color": "YELLOW"},
            {"action": "mark_frontier", "target_id": "g1", "node_id": "B", "color": "ORANGE"},
            {"action": "mark_visited", "target_id": "g1", "node_id": "B", "color": "GREEN"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "B"},
            {"action": "mark_frontier", "target_id": "g1", "node_id": "C", "color": "ORANGE"},
            {"action": "mark_visited", "target_id": "g1", "node_id": "C", "color": "GREEN"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "C"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "A"},
            {"action": "highlight_node", "target_id": "g1", "node_id": "B", "color": "YELLOW"},
            {"action": "mark_frontier", "target_id": "g1", "node_id": "D", "color": "ORANGE"},
            {"action": "mark_visited", "target_id": "g1", "node_id": "D", "color": "GREEN"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "D"},
            {"action": "mark_frontier", "target_id": "g1", "node_id": "E", "color": "ORANGE"},
            {"action": "mark_visited", "target_id": "g1", "node_id": "E", "color": "GREEN"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "E"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "B"},
            {"action": "highlight_node", "target_id": "g1", "node_id": "C", "color": "YELLOW"},
            {"action": "mark_frontier", "target_id": "g1", "node_id": "F", "color": "ORANGE"},
            {"action": "mark_visited", "target_id": "g1", "node_id": "F", "color": "GREEN"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "F"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "C"},
            {"action": "highlight_node", "target_id": "g1", "node_id": "D", "color": "YELLOW"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "D"},
            {"action": "highlight_node", "target_id": "g1", "node_id": "E", "color": "YELLOW"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "E"},
            {"action": "highlight_node", "target_id": "g1", "node_id": "F", "color": "YELLOW"},
            {"action": "unhighlight_node", "target_id": "g1", "node_id": "F"}
        ]

        graphs = {}
        node_states = {}

        for step in state_trace:
            action = step["action"]

            if action == "create_graph":
                tid = step["id"]
                positions = {
                    "A": LEFT * 3 + UP * 1.5,
                    "B": LEFT * 1.5 + UP * 0.2,
                    "C": RIGHT * 1.5 + UP * 0.2,
                    "D": LEFT * 2.5 + DOWN * 1.5,
                    "E": ORIGIN + DOWN * 1.5,
                    "F": RIGHT * 2.5 + DOWN * 1.5,
                }
                node_map = {}
                for node_id in step["nodes"]:
                    circle = Circle(radius=0.45, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2).set_fill(self.COLOR_DEFAULT)
                    label = Text(str(node_id), font_size=self.FONT_SIZE, color=WHITE)
                    label.move_to(circle.get_center())
                    node = VGroup(circle, label).move_to(positions[node_id])
                    node_map[node_id] = node
                    node_states[node_id] = self.COLOR_DEFAULT

                lines = VGroup(*[
                    Line(node_map[src].get_center(), node_map[dst].get_center())
                    for src, dst in step["edges"]
                ])
                graphs[tid] = node_map
                self.play(FadeIn(lines), *[FadeIn(node) for node in node_map.values()], run_time=0.8)

            elif action == "highlight_node":
                node = graphs[step["target_id"]][step["node_id"]]
                self.play(node[0].animate.set_fill(self.COLOR_CURRENT), run_time=0.3)
                node_states[step["node_id"]] = self.COLOR_CURRENT

            elif action == "mark_frontier":
                node = graphs[step["target_id"]][step["node_id"]]
                self.play(node[0].animate.set_fill(self.COLOR_FRONTIER), run_time=0.25)
                node_states[step["node_id"]] = self.COLOR_FRONTIER

            elif action == "mark_visited":
                node = graphs[step["target_id"]][step["node_id"]]
                self.play(node[0].animate.set_fill(self.COLOR_VISITED), run_time=0.25)
                node_states[step["node_id"]] = self.COLOR_VISITED

            elif action == "unhighlight_node":
                node = graphs[step["target_id"]][step["node_id"]]
                fallback = self.COLOR_VISITED if node_states[step["node_id"]] == self.COLOR_VISITED else self.COLOR_DEFAULT
                self.play(node[0].animate.set_fill(fallback), run_time=0.2)
                node_states[step["node_id"]] = fallback

            self.wait(0.2)

        self.wait(1.0)
