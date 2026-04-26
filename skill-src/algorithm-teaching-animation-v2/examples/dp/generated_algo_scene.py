from manim import *


class AlgorithmAnimation(Scene):
    CELL_SIZE = 0.9
    FONT_SIZE = 28

    COLOR_DEFAULT = BLUE_D
    COLOR_CURRENT = YELLOW
    COLOR_DEP = ORANGE
    COLOR_DONE = GREEN_D

    def construct(self):
        state_trace = [
            {"action": "create_matrix", "id": "dp", "rows": 3, "cols": 3, "values": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]},
            {"action": "highlight_cell", "target_id": "dp", "row": 1, "col": 1, "color": "YELLOW"},
            {"action": "highlight_cell", "target_id": "dp", "row": 0, "col": 1, "color": "ORANGE"},
            {"action": "highlight_cell", "target_id": "dp", "row": 0, "col": 0, "color": "ORANGE"},
            {"action": "set_cell", "target_id": "dp", "row": 1, "col": 1, "new_value": 1},
            {"action": "mark_cell", "target_id": "dp", "row": 1, "col": 1, "color": "GREEN"},
            {"action": "unhighlight_cell", "target_id": "dp", "row": 0, "col": 1},
            {"action": "unhighlight_cell", "target_id": "dp", "row": 0, "col": 0},
            {"action": "highlight_cell", "target_id": "dp", "row": 1, "col": 2, "color": "YELLOW"},
            {"action": "highlight_cell", "target_id": "dp", "row": 0, "col": 2, "color": "ORANGE"},
            {"action": "highlight_cell", "target_id": "dp", "row": 0, "col": 1, "color": "ORANGE"},
            {"action": "set_cell", "target_id": "dp", "row": 1, "col": 2, "new_value": 1},
            {"action": "mark_cell", "target_id": "dp", "row": 1, "col": 2, "color": "GREEN"},
            {"action": "unhighlight_cell", "target_id": "dp", "row": 0, "col": 2},
            {"action": "unhighlight_cell", "target_id": "dp", "row": 0, "col": 1},
            {"action": "highlight_cell", "target_id": "dp", "row": 2, "col": 2, "color": "YELLOW"},
            {"action": "highlight_cell", "target_id": "dp", "row": 1, "col": 2, "color": "ORANGE"},
            {"action": "highlight_cell", "target_id": "dp", "row": 1, "col": 0, "color": "ORANGE"},
            {"action": "set_cell", "target_id": "dp", "row": 2, "col": 2, "new_value": 3},
            {"action": "mark_cell", "target_id": "dp", "row": 2, "col": 2, "color": "GREEN"},
            {"action": "unhighlight_cell", "target_id": "dp", "row": 1, "col": 2},
            {"action": "unhighlight_cell", "target_id": "dp", "row": 1, "col": 0}
        ]

        matrices = {}

        for step in state_trace:
            action = step["action"]

            if action == "create_matrix":
                tid = step["id"]
                rows = step["rows"]
                cols = step["cols"]
                values = step["values"]

                cell_rows = []
                for r in range(rows):
                    row_cells = []
                    for c in range(cols):
                        rect = Square(side_length=self.CELL_SIZE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2)
                        rect.set_fill(self.COLOR_DEFAULT)
                        label = Text(str(values[r][c]), font_size=self.FONT_SIZE, color=WHITE)
                        label.move_to(rect.get_center())
                        cell = VGroup(rect, label)
                        row_cells.append(cell)
                    row_group = VGroup(*row_cells).arrange(RIGHT, buff=0)
                    cell_rows.append(row_group)

                matrix_group = VGroup(*cell_rows).arrange(DOWN, buff=0).move_to(ORIGIN)
                matrices[tid] = [[cell_rows[r][c] for c in range(cols)] for r in range(rows)]
                self.play(FadeIn(matrix_group), run_time=0.6)

            elif action == "highlight_cell":
                cell = matrices[step["target_id"]][step["row"]][step["col"]]
                color_name = step.get("color", "YELLOW")
                target_color = self.COLOR_CURRENT if color_name == "YELLOW" else self.COLOR_DEP
                self.play(cell[0].animate.set_fill(target_color), run_time=0.25)

            elif action == "unhighlight_cell":
                cell = matrices[step["target_id"]][step["row"]][step["col"]]
                current = cell[0].get_fill_color()
                fallback = self.COLOR_DONE if current == self.COLOR_DONE else self.COLOR_DEFAULT
                self.play(cell[0].animate.set_fill(fallback), run_time=0.2)

            elif action == "set_cell":
                cell = matrices[step["target_id"]][step["row"]][step["col"]]
                old_text = cell[1]
                new_text = Text(str(step["new_value"]), font_size=self.FONT_SIZE, color=WHITE)
                new_text.move_to(old_text.get_center())
                self.play(FadeOut(old_text), FadeIn(new_text), run_time=0.3)
                cell.remove(old_text)
                cell.add(new_text)

            elif action == "mark_cell":
                cell = matrices[step["target_id"]][step["row"]][step["col"]]
                self.play(cell[0].animate.set_fill(self.COLOR_DONE), run_time=0.25)

            self.wait(0.2)

        self.wait(1.0)
