from __future__ import annotations

import argparse
import importlib.util
import os
import sys
import traceback
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType


ACTIVE_VISIBLE_AUDITOR = None
VISIBLE_LEVEL_ORDER = {"error": 3, "warning": 2, "info": 1}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a Manim scene far enough to execute layout audits without rendering video.",
    )
    parser.add_argument("scene_file", help="Path to the generated Manim scene file.")
    parser.add_argument("scene_class", nargs="?", help="Scene class name. Defaults to the first Scene subclass.")
    parser.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Set MANIM_LAYOUT_AUDIT_FAIL=1 so LayoutAudit findings fail the run.",
    )
    parser.add_argument(
        "--audit-visible",
        action="store_true",
        help="Audit visible scene mobjects after each play() and at the end of construct().",
    )
    parser.add_argument(
        "--visible-final-only",
        action="store_true",
        help="With --audit-visible, scan only after construct() instead of after every play().",
    )
    parser.add_argument(
        "--visible-frame-margin",
        type=float,
        default=0.0,
        help="Frame margin for --audit-visible overflow checks.",
    )
    parser.add_argument(
        "--visible-containment-padding",
        type=float,
        default=1e-3,
        help="Required gap from outer boundaries before --audit-visible reports strict containment as info.",
    )
    parser.add_argument(
        "--visible-overlap-epsilon",
        type=float,
        default=1e-6,
        help="Minimum positive overlap width and height before --audit-visible reports overlap as warning.",
    )
    parser.add_argument(
        "--visible-include-descendants",
        action="store_true",
        help="Include descendants of non-container mobjects. This is noisier and usually not needed.",
    )
    parser.add_argument(
        "--visible-max-reports",
        type=int,
        default=250,
        help="Maximum number of unique visible-audit messages to print. Errors and warnings still affect exit status.",
    )
    parser.add_argument(
        "--visible-report-level",
        choices=("error", "warning", "info"),
        default="warning",
        help="Minimum visible-audit report level to print. Defaults to warning, which suppresses strict-containment info logs.",
    )
    parser.add_argument(
        "--traceback",
        action="store_true",
        help="Print a full traceback if scene construction fails.",
    )
    return parser.parse_args()


class VisibleAuditAccumulator:
    def __init__(self, args: argparse.Namespace, scene_class_name: str):
        self.args = args
        self.scene_class_name = scene_class_name
        self.play_index = 0
        self.error_count = 0
        self.warning_count = 0
        self.info_count = 0
        self.printed_count = 0
        self.limit_notice_printed = False
        self.seen_messages: set[tuple[str, str]] = set()

    def after_play(self, scene) -> None:
        if self.args.visible_final_only:
            return

        self.play_index += 1
        self.audit(scene, f"{self.scene_class_name}:after-play-{self.play_index:04d}")

    def final(self, scene) -> None:
        self.audit(scene, f"{self.scene_class_name}:final")

    def audit(self, scene, context: str) -> None:
        from visible_mobject_audit import audit_scene_visible_mobjects

        result = audit_scene_visible_mobjects(
            scene,
            context=context,
            frame_margin=self.args.visible_frame_margin,
            containment_padding=self.args.visible_containment_padding,
            overlap_epsilon=self.args.visible_overlap_epsilon,
            include_descendants=self.args.visible_include_descendants,
        )

        for message in result.errors:
            self._record("ERROR", result.context, message)
        for message in result.warnings:
            self._record("WARNING", result.context, message)
        for message in result.infos:
            self._record("INFO", result.context, message)

    def _record(self, level: str, context: str, message: str) -> None:
        key = (level, self._dedupe_signature(message))
        if key in self.seen_messages:
            return

        self.seen_messages.add(key)
        if level == "ERROR":
            self.error_count += 1
        elif level == "WARNING":
            self.warning_count += 1
        else:
            self.info_count += 1

        if not self._should_print(level):
            return

        if self.printed_count < self.args.visible_max_reports:
            prefix = f"[visible-layout:{context}]"
            print(f"{prefix} {level} {message}")
            self.printed_count += 1
            return

        if not self.limit_notice_printed:
            print(
                f"[layout-runner] "
                f"visible report limit reached ({self.args.visible_max_reports}); suppressing further unique messages"
            )
            self.limit_notice_printed = True

    def _should_print(self, level: str) -> bool:
        current = VISIBLE_LEVEL_ORDER[level.lower()]
        minimum = VISIBLE_LEVEL_ORDER[self.args.visible_report_level]
        return current >= minimum

    def _dedupe_signature(self, message: str) -> str:
        if "overlaps" in message:
            relation = "overlaps"
        elif "is strictly inside" in message:
            relation = "inside"
        elif "exceeds left frame" in message:
            relation = "exceeds-left"
        elif "exceeds right frame" in message:
            relation = "exceeds-right"
        elif "exceeds bottom frame" in message:
            relation = "exceeds-bottom"
        elif "exceeds top frame" in message:
            relation = "exceeds-top"
        else:
            relation = "other"

        bounds = message[message.find("(") :] if "(" in message else message
        return f"{relation}:{bounds}"


def load_module(scene_file: Path) -> ModuleType:
    module_name = f"_manim_layout_audit_target_{scene_file.stem}"
    spec = importlib.util.spec_from_file_location(module_name, scene_file)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load scene file: {scene_file}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def find_scene_class(module: ModuleType, requested_name: str | None):
    from manim import Scene

    if requested_name:
        scene_class = getattr(module, requested_name, None)
        if scene_class is None:
            raise RuntimeError(f"Scene class not found: {requested_name}")
        if not isinstance(scene_class, type) or not issubclass(scene_class, Scene):
            raise RuntimeError(f"{requested_name} is not a Manim Scene subclass")
        return scene_class

    scene_classes = [
        value
        for value in module.__dict__.values()
        if isinstance(value, type) and issubclass(value, Scene) and value is not Scene and value.__module__ == module.__name__
    ]
    if not scene_classes:
        raise RuntimeError("No Manim Scene subclass found in scene file")
    if len(scene_classes) > 1:
        names = ", ".join(cls.__name__ for cls in scene_classes)
        raise RuntimeError(f"Multiple Scene subclasses found; pass one explicitly: {names}")
    return scene_classes[0]


def flatten_animations(animation):
    children = getattr(animation, "animations", None)
    if children:
        for child in children:
            yield from flatten_animations(child)
    else:
        yield animation


def finish_animation(scene, animation) -> None:
    from manim import Animation

    if not isinstance(animation, Animation):
        raise TypeError(f"Scene.play expected Animation instances; got {type(animation).__name__}")

    mobject = getattr(animation, "mobject", None)
    if mobject is not None:
        scene.add(mobject)

    animation.begin()
    animation.interpolate(1)
    animation.finish()
    animation.clean_up_from_scene(scene)


def dry_play(scene, *animations, **kwargs):
    animations = scene.compile_animations(*animations, **kwargs)
    for animation in animations:
        for child in flatten_animations(animation):
            finish_animation(scene, child)
    if ACTIVE_VISIBLE_AUDITOR is not None:
        ACTIVE_VISIBLE_AUDITOR.after_play(scene)
    return scene


def dry_wait(scene, *args, **kwargs):
    return scene


def dry_add_sound(scene, *args, **kwargs):
    return scene


@contextmanager
def patched_scene_methods(visible_auditor=None):
    from manim import Scene

    global ACTIVE_VISIBLE_AUDITOR

    original_play = Scene.play
    original_wait = Scene.wait
    original_add_sound = getattr(Scene, "add_sound", None)
    original_visible_auditor = ACTIVE_VISIBLE_AUDITOR

    Scene.play = dry_play
    Scene.wait = dry_wait
    if original_add_sound is not None:
        Scene.add_sound = dry_add_sound
    ACTIVE_VISIBLE_AUDITOR = visible_auditor

    try:
        yield
    finally:
        ACTIVE_VISIBLE_AUDITOR = original_visible_auditor
        Scene.play = original_play
        Scene.wait = original_wait
        if original_add_sound is not None:
            Scene.add_sound = original_add_sound


def main() -> int:
    args = parse_args()
    scene_file = Path(args.scene_file).resolve()
    if not scene_file.exists():
        print(f"[layout-runner] scene file not found: {scene_file}", file=sys.stderr)
        return 2

    script_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(script_dir))
    sys.path.insert(0, str(scene_file.parent))

    os.environ.setdefault("MANIM_LAYOUT_AUDIT", "1")
    if args.fail_on_warning:
        os.environ["MANIM_LAYOUT_AUDIT_FAIL"] = "1"
    os.environ["MANIM_LAYOUT_DRY_RUN"] = "1"

    try:
        module = load_module(scene_file)
        scene_class = find_scene_class(module, args.scene_class)
        visible_auditor = VisibleAuditAccumulator(args, scene_class.__name__) if args.audit_visible else None
        with patched_scene_methods(visible_auditor):
            scene = scene_class()
            scene.construct()
            if visible_auditor is not None:
                visible_auditor.final(scene)
    except Exception as exc:
        print(f"[layout-runner] failed: {exc}", file=sys.stderr)
        if args.traceback:
            traceback.print_exc()
        return 1

    print(f"[layout-runner] completed dry-run for {scene_class.__name__}")
    if (
        args.fail_on_warning
        and visible_auditor is not None
        and (visible_auditor.error_count or visible_auditor.warning_count)
    ):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
