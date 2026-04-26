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
    COLOR_SORTED = GREEN_D
    COLOR_POINTER = MAROON_B

    def construct(self):
        state_trace = [
            {"action": "create_array", "id": "main", "values": [5, 1, 4, 2, 8]},
            {"action": "create_pointer", "id": "p_j", "label": "j", "target_id": "main", "index": 0, "position": "top"},
            {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 0},
            {"action": "highlight", "target_id": "main", "indices": [0, 1], "color": "YELLOW"},
            {"action": "swap", "target_id": "main", "i": 0, "j": 1},
            {"action": "unhighlight", "target_id": "main", "indices": [0, 1]},
            {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 1},
            {"action": "highlight", "target_id": "main", "indices": [1, 2], "color": "YELLOW"},
            {"action": "swap", "target_id": "main", "i": 1, "j": 2},
            {"action": "unhighlight", "target_id": "main", "indices": [1, 2]},
            {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 2},
            {"action": "highlight", "target_id": "main", "indices": [2, 3], "color": "YELLOW"},
            {"action": "swap", "target_id": "main", "i": 2, "j": 3},
            {"action": "unhighlight", "target_id": "main", "indices": [2, 3]},
            {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 3},
            {"action": "highlight", "target_id": "main", "indices": [3, 4], "color": "YELLOW"},
            {"action": "unhighlight", "target_id": "main", "indices": [3, 4]},
            {"action": "mark_sorted", "target_id": "main", "indices": [4]},
            {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 0},
            {"action": "highlight", "target_id": "main", "indices": [0, 1], "color": "YELLOW"},
            {"action": "unhighlight", "target_id": "main", "indices": [0, 1]},
            {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 1},
            {"action": "highlight", "target_id": "main", "indices": [1, 2], "color": "YELLOW"},
            {"action": "swap", "target_id": "main", "i": 1, "j": 2},
            {"action": "unhighlight", "target_id": "main", "indices": [1, 2]},
            {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 2},
            {"action": "highlight", "target_id": "main", "indices": [2, 3], "color": "YELLOW"},
            {"action": "unhighlight", "target_id": "main", "indices": [2, 3]},
            {"action": "mark_sorted", "target_id": "main", "indices": [3]},
            {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 0},
            {"action": "highlight", "target_id": "main", "indices": [0, 1], "color": "YELLOW"},
            {"action": "unhighlight", "target_id": "main", "indices": [0, 1]},
            {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 1},
            {"action": "highlight", "target_id": "main", "indices": [1, 2], "color": "YELLOW"},
            {"action": "unhighlight", "target_id": "main", "indices": [1, 2]},
            {"action": "mark_sorted", "target_id": "main", "indices": [2]},
            {"action": "move_pointer", "id": "p_j", "target_id": "main", "index": 0},
            {"action": "highlight", "target_id": "main", "indices": [0, 1], "color": "YELLOW"},
            {"action": "unhighlight", "target_id": "main", "indices": [0, 1]},
            {"action": "mark_sorted", "target_id": "main", "indices": [1]},
            {"action": "mark_sorted", "target_id": "main", "indices": [0]},
            {"action": "remove_pointer", "id": "p_j"}
        ]

        arrays = {}
        pointers = {}

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

                group = VGroup(*elems).arrange(RIGHT, buff=self.ELEM_BUFF).move_to(UP * 0.5)
                arrays[tid] = elems

                index_labels = VGroup()
                for idx, elem in enumerate(elems):
                    index_text = Text(str(idx), font_size=self.INDEX_FONT_SIZE, color=GREY_C)
                    index_text.next_to(elem, DOWN, buff=0.25)
                    index_labels.add(index_text)

                self.play(FadeIn(group), FadeIn(index_labels), run_time=0.6)

            elif action == "create_pointer":
                pid = step["id"]
                target = arrays[step["target_id"]][step["index"]]

                triangle = Triangle(color=self.COLOR_POINTER, fill_opacity=1.0).scale(0.2).rotate(PI)
                label = Text(step["label"], font_size=24, color=self.COLOR_POINTER)
                label.next_to(triangle, DOWN, buff=0.1)
                pointer = VGroup(triangle, label)
                pointer.next_to(target, UP, buff=self.POINTER_BUFF)
                pointers[pid] = pointer
                self.play(FadeIn(pointer), run_time=0.4)

            elif action == "move_pointer":
                pid = step["id"]
                target = arrays[step["target_id"]][step["index"]]
                self.play(pointers[pid].animate.next_to(target, UP, buff=self.POINTER_BUFF), run_time=0.35)

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
                    target_color = self.COLOR_SORTED if rect.get_fill_color() == self.COLOR_SORTED else self.COLOR_DEFAULT
                    animations.append(rect.animate.set_fill(target_color))
                self.play(*animations, run_time=0.25)

            elif action == "swap":
                tid = step["target_id"]
                i = step["i"]
                j = step["j"]
                pos_i = arrays[tid][i].get_center()
                pos_j = arrays[tid][j].get_center()

                self.play(
                    arrays[tid][i].animate.move_to(pos_j),
                    arrays[tid][j].animate.move_to(pos_i),
                    run_time=0.6,
                )

                arrays[tid][i], arrays[tid][j] = arrays[tid][j], arrays[tid][i]

            elif action == "mark_sorted":
                tid = step["target_id"]
                self.play(
                    *[arrays[tid][i][0].animate.set_fill(self.COLOR_SORTED) for i in step["indices"]],
                    run_time=0.3,
                )

            elif action == "remove_pointer":
                pid = step["id"]
                self.play(FadeOut(pointers[pid]), run_time=0.3)
                del pointers[pid]

            self.wait(0.2)

        self.wait(1.0)
