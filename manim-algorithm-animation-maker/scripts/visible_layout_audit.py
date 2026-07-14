from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from manim import config


CONTAINER_TYPE_NAMES = {"Group", "VGroup"}
EPSILON = 1e-6


@dataclass(frozen=True)
class Bounds:
    left: float
    right: float
    bottom: float
    top: float

    @property
    def width(self) -> float:
        return self.right - self.left

    @property
    def height(self) -> float:
        return self.top - self.bottom

    @property
    def area(self) -> float:
        return max(0.0, self.width) * max(0.0, self.height)

    def format(self) -> str:
        return (
            f"left={self.left:.2f}, right={self.right:.2f}, "
            f"bottom={self.bottom:.2f}, top={self.top:.2f}"
        )


@dataclass(frozen=True)
class VisibleItem:
    name: str
    mobject: object
    bounds: Bounds


@dataclass
class VisibleAuditResult:
    context: str
    errors: list[str]
    warnings: list[str]
    infos: list[str]

    def emit(self) -> None:
        prefix = f"[visible-layout:{self.context}]" if self.context else "[visible-layout]"
        for message in self.errors:
            print(f"{prefix} ERROR {message}")
        for message in self.warnings:
            print(f"{prefix} WARNING {message}")
        for message in self.infos:
            print(f"{prefix} INFO {message}")


def audit_scene_visible_mobjects(
    scene,
    context: str = "visible",
    frame_margin: float = 0.0,
    containment_padding: float = 1e-3,
    overlap_epsilon: float = EPSILON,
    include_descendants: bool = False,
) -> VisibleAuditResult:
    items = collect_visible_items(scene.mobjects, include_descendants=include_descendants)
    errors: list[str] = []
    warnings: list[str] = []
    infos: list[str] = []

    half_width = config.frame_width / 2
    half_height = config.frame_height / 2

    for item in items:
        bounds = item.bounds
        if bounds.left < -half_width + frame_margin:
            errors.append(f"{item.name}: exceeds left frame ({bounds.format()})")
        if bounds.right > half_width - frame_margin:
            errors.append(f"{item.name}: exceeds right frame ({bounds.format()})")
        if bounds.bottom < -half_height + frame_margin:
            errors.append(f"{item.name}: exceeds bottom frame ({bounds.format()})")
        if bounds.top > half_height - frame_margin:
            errors.append(f"{item.name}: exceeds top frame ({bounds.format()})")

    for index, first in enumerate(items):
        for second in items[index + 1 :]:
            relation = classify_pair(first.bounds, second.bounds, containment_padding, overlap_epsilon)
            if relation == "first-inside-second":
                infos.append(f"{first.name}: is strictly inside {second.name} ({first.bounds.format()}; {second.bounds.format()})")
            elif relation == "second-inside-first":
                infos.append(f"{second.name}: is strictly inside {first.name} ({second.bounds.format()}; {first.bounds.format()})")
            elif relation == "overlap":
                warnings.append(f"{first.name}: overlaps {second.name} ({first.bounds.format()}; {second.bounds.format()})")

    return VisibleAuditResult(context=context, errors=errors, warnings=warnings, infos=infos)


def collect_visible_items(mobjects: Iterable[object], include_descendants: bool = False) -> list[VisibleItem]:
    items: list[VisibleItem] = []
    seen: set[int] = set()

    def visit(mobject, path: str) -> None:
        if id(mobject) in seen:
            return

        children = list(getattr(mobject, "submobjects", []) or [])
        is_container = type(mobject).__name__ in CONTAINER_TYPE_NAMES
        should_collect = include_descendants or not is_container or not children

        if should_collect and is_visible_mobject(mobject):
            seen.add(id(mobject))
            items.append(VisibleItem(path, mobject, get_bounds(mobject)))
            if not include_descendants:
                return

        if children:
            for child_index, child in enumerate(children):
                visit(child, f"{path}.{type(child).__name__}[{child_index}]")

    for index, mobject in enumerate(mobjects):
        visit(mobject, f"{type(mobject).__name__}[{index}]")

    return items


def is_visible_mobject(mobject) -> bool:
    try:
        bounds = get_bounds(mobject)
    except Exception:
        return False

    if bounds.width <= EPSILON or bounds.height <= EPSILON:
        return False

    fill_opacity = max_opacity(call_zero_arg(mobject, "get_fill_opacity", 0.0))
    stroke_opacity = max_opacity(call_zero_arg(mobject, "get_stroke_opacity", 0.0))
    has_children = bool(getattr(mobject, "submobjects", []) or [])
    return fill_opacity > EPSILON or stroke_opacity > EPSILON or has_children


def get_bounds(mobject) -> Bounds:
    return Bounds(
        left=float(mobject.get_left()[0]),
        right=float(mobject.get_right()[0]),
        bottom=float(mobject.get_bottom()[1]),
        top=float(mobject.get_top()[1]),
    )


def classify_pair(
    first: Bounds,
    second: Bounds,
    containment_padding: float,
    overlap_epsilon: float,
) -> str:
    first_inside_second = is_strictly_inside(first, second, containment_padding)
    second_inside_first = is_strictly_inside(second, first, containment_padding)
    if first_inside_second:
        return "first-inside-second"
    if second_inside_first:
        return "second-inside-first"

    x_overlap = min(first.right, second.right) - max(first.left, second.left)
    y_overlap = min(first.top, second.top) - max(first.bottom, second.bottom)
    if x_overlap > overlap_epsilon and y_overlap > overlap_epsilon:
        return "overlap"
    return "separate"


def is_strictly_inside(inner: Bounds, outer: Bounds, padding: float) -> bool:
    return (
        inner.area < outer.area
        and inner.left > outer.left + padding
        and inner.right < outer.right - padding
        and inner.bottom > outer.bottom + padding
        and inner.top < outer.top - padding
    )


def call_zero_arg(mobject, method_name: str, default):
    method = getattr(mobject, method_name, None)
    if method is None:
        return default
    try:
        return method()
    except Exception:
        return default


def max_opacity(value) -> float:
    try:
        if isinstance(value, (str, bytes)):
            return 0.0
        return float(max(value))
    except TypeError:
        try:
            return float(value)
        except Exception:
            return 0.0
    except ValueError:
        return 0.0
