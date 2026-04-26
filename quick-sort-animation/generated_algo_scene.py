import json
from collections import OrderedDict
from pathlib import Path

from manim import *


class AlgorithmAnimation(Scene):
    ELEM_WIDTH = 0.85
    ELEM_HEIGHT = 0.8
    ELEM_BUFF = 0.12
    FONT_SIZE = 30
    INDEX_FONT_SIZE = 18
    POINTER_FONT_SIZE = 22
    NOTE_FONT_SIZE = 24
    POINTER_BUFF = 0.18
    MIN_BEAT_PAUSE = 0.15

    COLOR_DEFAULT = BLUE_D
    COLOR_HIGHLIGHT = YELLOW
    COLOR_PIVOT = ORANGE
    COLOR_SORTED = GREEN_D
    COLOR_POINTER_TOP = MAROON_B
    COLOR_POINTER_BOTTOM = TEAL_B
    COLOR_RANGE = GREY_B

    def construct(self):
        self.root = Path(__file__).resolve().parent
        self.trace = self.load_json("action_trace.json")
        self.manifest = self.load_json("narration_manifest.json")

        self.arrays = {}
        self.array_states = {}
        self.pointers = {}
        self.active_ranges = {}
        self.index_labels = {}
        self.note = None

        title = Text("Quick Sort: rightmost pivot", font_size=34, color=WHITE)
        title.to_edge(UP, buff=0.25)
        self.play(FadeIn(title), run_time=0.4)

        actions_by_beat = self.group_actions_by_beat(self.trace)
        for segment in self.manifest["segments"]:
            beat_id = segment["beat_id"]
            audio_path = self.root / segment["audio_path"]
            if audio_path.exists():
                self.add_sound(str(audio_path))

            elapsed = 0
            for action in actions_by_beat.get(beat_id, []):
                elapsed += self.apply_action(action)

            wait_time = max(float(segment["duration_seconds"]) - elapsed, self.MIN_BEAT_PAUSE)
            self.wait(wait_time)

        self.wait(1.0)

    def load_json(self, name):
        path = self.root / name
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def group_actions_by_beat(self, trace):
        grouped = OrderedDict()
        for action in trace:
            grouped.setdefault(action["beat_id"], []).append(action)
        return grouped

    def apply_action(self, step):
        action = step["action"]

        if action == "set_note":
            return self.set_note(step["text"])
        if action == "create_array":
            return self.create_array(step)
        if action == "set_active_range":
            return self.set_active_range(step)
        if action == "clear_active_range":
            return self.clear_active_range(step)
        if action == "create_pointer":
            return self.create_pointer(step)
        if action == "move_pointer":
            return self.move_pointer(step)
        if action == "remove_pointer":
            return self.remove_pointer(step)
        if action == "highlight":
            return self.highlight(step)
        if action == "unhighlight":
            return self.unhighlight(step)
        if action == "swap":
            return self.swap(step)
        if action == "mark_sorted":
            return self.mark_sorted(step)

        raise ValueError(f"Unsupported action: {action}")

    def set_note(self, text):
        new_note = Text(text, font_size=self.NOTE_FONT_SIZE, color=GREY_A)
        new_note.next_to(ORIGIN, UP, buff=2.25)

        if self.note is None:
            self.note = new_note
            self.play(FadeIn(self.note), run_time=0.25)
        else:
            self.play(Transform(self.note, new_note), run_time=0.25)
        return 0.25

    def create_array(self, step):
        tid = step["id"]
        elems = []
        states = []
        for value in step["values"]:
            rect = RoundedRectangle(
                corner_radius=0.08,
                width=self.ELEM_WIDTH,
                height=self.ELEM_HEIGHT,
                fill_opacity=0.92,
                stroke_color=WHITE,
                stroke_width=2,
            ).set_fill(self.COLOR_DEFAULT)
            label = Text(str(value), font_size=self.FONT_SIZE, color=WHITE)
            label.move_to(rect.get_center())
            elems.append(VGroup(rect, label))
            states.append("default")

        group = VGroup(*elems).arrange(RIGHT, buff=self.ELEM_BUFF).move_to(DOWN * 0.15)
        labels = VGroup()
        for idx, elem in enumerate(elems):
            index_text = Text(str(idx), font_size=self.INDEX_FONT_SIZE, color=GREY_C)
            index_text.next_to(elem, DOWN, buff=0.18)
            labels.add(index_text)

        self.arrays[tid] = elems
        self.array_states[tid] = states
        self.index_labels[tid] = labels
        self.play(FadeIn(group), FadeIn(labels), run_time=0.6)
        return 0.6

    def set_active_range(self, step):
        tid = step["target_id"]
        if tid in self.active_ranges:
            self.play(FadeOut(self.active_ranges[tid]), run_time=0.15)

        start = step["start"]
        end = step["end"]
        elems = self.arrays[tid][start : end + 1]
        box = SurroundingRectangle(
            VGroup(*elems),
            color=self.COLOR_RANGE,
            buff=0.16,
            stroke_width=3,
        )
        range_group = VGroup(box)
        self.active_ranges[tid] = range_group
        self.play(FadeIn(range_group), run_time=0.25)
        return 0.4

    def clear_active_range(self, step):
        tid = step["target_id"]
        if tid not in self.active_ranges:
            return 0
        self.play(FadeOut(self.active_ranges[tid]), run_time=0.2)
        del self.active_ranges[tid]
        return 0.2

    def create_pointer(self, step):
        pid = step["id"]
        color = self.COLOR_POINTER_TOP if step["position"] == "top" else self.COLOR_POINTER_BOTTOM
        triangle = Triangle(color=color, fill_opacity=1.0).scale(0.16)
        label = Text(step["label"], font_size=self.POINTER_FONT_SIZE, color=color)

        if step["position"] == "top":
            triangle.rotate(PI)
            label.next_to(triangle, UP, buff=0.04)
        else:
            label.next_to(triangle, DOWN, buff=0.04)

        pointer = VGroup(triangle, label)
        pointer.move_to(self.pointer_target_position(step["target_id"], step["index"], step["position"]))
        self.pointers[pid] = {"mobject": pointer, "position": step["position"]}
        self.play(FadeIn(pointer), run_time=0.25)
        return 0.25

    def move_pointer(self, step):
        pid = step["id"]
        if pid not in self.pointers:
            return 0
        pointer = self.pointers[pid]["mobject"]
        position = self.pointers[pid]["position"]
        target = self.pointer_target_position(step["target_id"], step["index"], position)
        self.play(pointer.animate.move_to(target), run_time=0.35)
        return 0.35

    def remove_pointer(self, step):
        pid = step["id"]
        if pid not in self.pointers:
            return 0
        self.play(FadeOut(self.pointers[pid]["mobject"]), run_time=0.2)
        del self.pointers[pid]
        return 0.2

    def highlight(self, step):
        tid = step["target_id"]
        color = self.color_from_name(step.get("color", "YELLOW"))
        animations = [self.arrays[tid][idx][0].animate.set_fill(color) for idx in step["indices"]]
        self.play(*animations, run_time=0.22)
        return 0.22

    def unhighlight(self, step):
        tid = step["target_id"]
        animations = []
        for idx in step["indices"]:
            animations.append(self.arrays[tid][idx][0].animate.set_fill(self.color_for_state(tid, idx)))
        self.play(*animations, run_time=0.22)
        return 0.22

    def swap(self, step):
        tid = step["target_id"]
        i = step["i"]
        j = step["j"]
        if i == j:
            return 0

        pos_i = self.arrays[tid][i].get_center()
        pos_j = self.arrays[tid][j].get_center()
        self.play(
            self.arrays[tid][i].animate.move_to(pos_j),
            self.arrays[tid][j].animate.move_to(pos_i),
            run_time=0.55,
        )
        self.arrays[tid][i], self.arrays[tid][j] = self.arrays[tid][j], self.arrays[tid][i]
        self.array_states[tid][i], self.array_states[tid][j] = self.array_states[tid][j], self.array_states[tid][i]
        return 0.55

    def mark_sorted(self, step):
        tid = step["target_id"]
        animations = []
        for idx in step["indices"]:
            self.array_states[tid][idx] = "sorted"
            animations.append(self.arrays[tid][idx][0].animate.set_fill(self.COLOR_SORTED))
        self.play(*animations, run_time=0.3)
        return 0.3

    def pointer_target_position(self, target_id, index, position):
        elems = self.arrays[target_id]
        if index < 0:
            target_x = elems[0].get_left()[0] - 0.34
            target_y = elems[0].get_center()[1]
            anchor = np.array([target_x, target_y, 0])
        elif index >= len(elems):
            target_x = elems[-1].get_right()[0] + 0.34
            target_y = elems[-1].get_center()[1]
            anchor = np.array([target_x, target_y, 0])
        else:
            anchor = elems[index].get_center()

        if position == "top":
            return anchor + UP * (self.ELEM_HEIGHT / 2 + self.POINTER_BUFF + 0.22)
        return anchor + DOWN * (self.ELEM_HEIGHT / 2 + self.POINTER_BUFF + 0.22)

    def color_for_state(self, target_id, index):
        if self.array_states[target_id][index] == "sorted":
            return self.COLOR_SORTED
        return self.COLOR_DEFAULT

    def color_from_name(self, name):
        return {
            "YELLOW": self.COLOR_HIGHLIGHT,
            "ORANGE": self.COLOR_PIVOT,
            "GREEN": self.COLOR_SORTED,
            "GREEN_D": self.COLOR_SORTED,
            "BLUE_D": self.COLOR_DEFAULT,
        }.get(name, self.COLOR_HIGHLIGHT)
