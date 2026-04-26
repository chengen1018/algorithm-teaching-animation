import json
from pathlib import Path


class AlgorithmTracer:
    def __init__(self):
        self.actions = []

    def _add(self, action, beat_id, **payload):
        event = {"seq": len(self.actions) + 1, "beat_id": beat_id, "action": action}
        event.update(payload)
        self.actions.append(event)

    def set_note(self, text, beat_id):
        self._add("set_note", beat_id, text=text)

    def create_array(self, array_id, values, beat_id):
        self._add("create_array", beat_id, id=array_id, values=list(values))

    def set_active_range(self, target_id, start, end, label, beat_id):
        self._add(
            "set_active_range",
            beat_id,
            target_id=target_id,
            start=start,
            end=end,
            label=label,
        )

    def clear_active_range(self, target_id, beat_id):
        self._add("clear_active_range", beat_id, target_id=target_id)

    def highlight(self, target_id, indices, color, beat_id):
        self._add("highlight", beat_id, target_id=target_id, indices=list(indices), color=color)

    def unhighlight(self, target_id, indices, beat_id):
        self._add("unhighlight", beat_id, target_id=target_id, indices=list(indices))

    def swap(self, target_id, i, j, beat_id):
        self._add("swap", beat_id, target_id=target_id, i=i, j=j)

    def mark_sorted(self, target_id, indices, beat_id):
        self._add("mark_sorted", beat_id, target_id=target_id, indices=list(indices))

    def create_pointer(self, pointer_id, label, target_id, index, beat_id, position="top"):
        self._add(
            "create_pointer",
            beat_id,
            id=pointer_id,
            label=label,
            target_id=target_id,
            index=index,
            position=position,
        )

    def move_pointer(self, pointer_id, target_id, index, beat_id):
        self._add("move_pointer", beat_id, id=pointer_id, target_id=target_id, index=index)

    def remove_pointer(self, pointer_id, beat_id):
        self._add("remove_pointer", beat_id, id=pointer_id)

    def output(self, path="action_trace.json"):
        out = Path(path)
        out.write_text(json.dumps(self.actions, indent=2), encoding="utf-8")

    def get_actions(self):
        return list(self.actions)

