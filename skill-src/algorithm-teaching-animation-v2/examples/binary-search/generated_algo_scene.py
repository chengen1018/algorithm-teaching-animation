from manim import *


class AlgorithmAnimation(Scene):
    ELEM_WIDTH = 0.9
    ELEM_HEIGHT = 0.9
    ELEM_BUFF = 0.15
    FONT_SIZE = 32
    POINTER_BUFF = 0.25
    INDEX_FONT_SIZE = 20

    COLOR_DEFAULT = BLUE_D
    COLOR_HIGHLIGHT = YELLOW
    COLOR_DIMMED = GREY_D
    COLOR_FOUND = GREEN_D
    COLOR_LEFT = MAROON_B
    COLOR_RIGHT = TEAL_D
    COLOR_MID = ORANGE

    def construct(self):
        state_trace = [
            {"action": "create_array", "id": "main", "values": [1, 3, 5, 7, 9, 11, 13]},
            {"action": "create_pointer", "id": "p_left", "label": "left", "target_id": "main", "index": 0, "position": "bottom"},
            {"action": "create_pointer", "id": "p_right", "label": "right", "target_id": "main", "index": 6, "position": "bottom"},
            {"action": "create_pointer", "id": "p_mid", "label": "mid", "target_id": "main", "index": 3, "position": "top"},
            {"action": "highlight", "target_id": "main", "indices": [3], "color": "YELLOW"},
            {"action": "mark_excluded", "target_id": "main", "indices": [0, 1, 2, 3]},
            {"action": "move_pointer", "id": "p_left", "target_id": "main", "index": 4},
            {"action": "remove_pointer", "id": "p_mid"},
            {"action": "create_pointer", "id": "p_mid", "label": "mid", "target_id": "main", "index": 5, "position": "top"},
            {"action": "highlight", "target_id": "main", "indices": [5], "color": "YELLOW"},
            {"action": "mark_sorted", "target_id": "main", "indices": [5]},
            {"action": "unhighlight", "target_id": "main", "indices": [5]},
            {"action": "remove_pointer", "id": "p_mid"},
            {"action": "remove_pointer", "id": "p_left"},
            {"action": "remove_pointer", "id": "p_right"}
        ]

        arrays = {}
        pointers = {}
        pointer_colors = {
            "p_left": self.COLOR_LEFT,
            "p_right": self.COLOR_RIGHT,
            "p_mid": self.COLOR_MID,
        }

        for step in state_trace:
            action = step["action"]

            if action == "create_array":
                tid = step["id"]
                elems = []
                for value in step["values"]:
                    rect = RoundedRectangle(
                        corner_radius=0.15,
                        width=self.ELEM_WIDTH,
                        height=self.ELEM_HEIGHT,
                        fill_opacity=0.9,
                        stroke_color=WHITE,
                        stroke_width=2,
                    ).set_fill(self.COLOR_DEFAULT)
                    label = Text(str(value), font_size=self.FONT_SIZE, color=WHITE)
                    label.move_to(rect.get_center())
                    elems.append(VGroup(rect, label))

                group = VGroup(*elems).arrange(RIGHT, buff=self.ELEM_BUFF).move_to(UP * 0.4)
                arrays[tid] = elems

                index_labels = VGroup()
                for idx, elem in enumerate(elems):
                    index_text = Text(str(idx), font_size=self.INDEX_FONT_SIZE, color=GREY_C)
                    index_text.next_to(elem, DOWN, buff=0.25)
                    index_labels.add(index_text)

                target_text = Text("target = 11", font_size=26, color=WHITE).to_edge(UP)
                self.play(FadeIn(group), FadeIn(index_labels), FadeIn(target_text), run_time=0.6)

            elif action == "create_pointer":
                pid = step["id"]
                target = arrays[step["target_id"]][step["index"]]
                color = pointer_colors.get(pid, WHITE)

                triangle = Triangle(color=color, fill_opacity=1.0).scale(0.2)
                label = Text(step["label"], font_size=22, color=color)

                if step["position"] == "top":
                    triangle.rotate(PI)
                    label.next_to(triangle, DOWN, buff=0.1)
                    pointer = VGroup(triangle, label)
                    pointer.next_to(target, UP, buff=self.POINTER_BUFF)
                else:
                    label.next_to(triangle, UP, buff=0.1)
                    pointer = VGroup(triangle, label)
                    pointer.next_to(target, DOWN, buff=0.55)

                pointers[pid] = (pointer, step["position"])
                self.play(FadeIn(pointer), run_time=0.35)

            elif action == "move_pointer":
                pid = step["id"]
                pointer, position = pointers[pid]
                target = arrays[step["target_id"]][step["index"]]
                direction = UP if position == "top" else DOWN
                buff = self.POINTER_BUFF if position == "top" else 0.55
                self.play(pointer.animate.next_to(target, direction, buff=buff), run_time=0.35)

            elif action == "highlight":
                tid = step["target_id"]
                self.play(
                    *[arrays[tid][i][0].animate.set_fill(self.COLOR_HIGHLIGHT) for i in step["indices"]],
                    run_time=0.25,
                )

            elif action == "unhighlight":
                tid = step["target_id"]
                animations = []
                for i in step["indices"]:
                    rect = arrays[tid][i][0]
                    if rect.get_fill_color() == self.COLOR_FOUND:
                        continue
                    animations.append(rect.animate.set_fill(self.COLOR_DEFAULT))
                if animations:
                    self.play(*animations, run_time=0.3)

            elif action == "mark_excluded":
                tid = step["target_id"]
                self.play(
                    *[arrays[tid][i][0].animate.set_fill(self.COLOR_DIMMED) for i in step["indices"]],
                    run_time=0.3,
                )

            elif action == "mark_sorted":
                tid = step["target_id"]
                self.play(
                    *[arrays[tid][i][0].animate.set_fill(self.COLOR_FOUND) for i in step["indices"]],
                    run_time=0.3,
                )

            elif action == "remove_pointer":
                pid = step["id"]
                pointer, _ = pointers[pid]
                self.play(FadeOut(pointer), run_time=0.25)
                del pointers[pid]

            self.wait(0.25)

        self.wait(1.0)
