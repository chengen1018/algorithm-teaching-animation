# Scene Layout Validator Contract

## Role boundary

`scene_layout_validator` is the pre-render layout-validation role. It uses the
layout-audit runner to execute the four approved Scene classes without formal
Manim rendering. The runner creates real Manim mobjects so geometry can be
checked, but it must not write frames or MP4 files. This role does not validate
rendered media.

## Required inputs

Before starting, read every coordinator-provided absolute path in full:

1. `<project-root>/generated_algo_scene.py`
2. `<project-root>/scene_code_review_handoff.md`
3. the `layout-audit.md` reference
4. the `run_layout_audit.py` runner

The coordinator must also identify the four delivered Scene class names and
their approved order. All input and output paths used in commands and the
result must be absolute paths.

## Preflight

- All required inputs and the runner exist and are readable.
- `scene_code_review_handoff.md` identifies the exact `generated_algo_scene.py`
  under audit and its SHA-256.
- The handoff's four-Scene contract identifies exactly four delivered Scene
  classes in order.
- The runner is the supplied non-render layout runner; its documented behavior
  does not invoke a formal `manim` render or write video output.

If preflight cannot be completed, write `layout_audit_result.md` with
`Result: FAIL`, the failed preflight evidence, and the code hash when it can be
calculated. Do not substitute another source, runner, Scene list, or inferred
order.

## Forbidden actions

- Do not run formal Manim rendering commands, including `manim` or
  `python -m manim`.
- Do not create frames, MP4 files, previews, or any other rendered media.
- Do not modify `generated_algo_scene.py`, the handoff, the runner, the audit
  reference, or any upstream artifact.
- Do not change the layout runner's geometry algorithm, hide warnings, truncate
  output, omit a Scene, or manually waive a finding.

## Procedure

1. Record the absolute code path and calculate its SHA-256 before running the
   audit.
2. Record the following named layout-affecting evidence fields before the
   first required audit command. None of these fields may be replaced by an
   opaque "environment" summary:

   - `Runner path` and `Runner SHA-256`
   - `Python version`
   - `Manim version`
   - `Frame width`
   - `Frame height`
   - `Renderer/profile/quality`
   - `Font/font-resolution evidence` (the requested font names, the resolved
     font files or fallback names used by Manim/Pango, and file hashes when a
     resolved local font file is available)

   Also record the relevant runner options and any additional operating-system
   or environment details needed to reproduce those named values. If a named
   field cannot be determined, the result cannot be `PASS`.
3. For each of the four approved Scene classes, in approved order, run exactly
   this non-rendering layout audit and capture complete stdout and stderr:

   ```bash
   python <absolute-runner-path> <absolute-project-root>/generated_algo_scene.py <SceneClass> --audit-visible --fail-on-warning --visible-report-level warning
   ```

4. Record each complete command and exit code. A supplementary
   `--visible-report-level info` invocation may document strict containment,
   but cannot replace or alter the warning-level verdict.
5. Write `<project-root>/layout_audit_result.md`. It must contain `Result: PASS`
   or `Result: FAIL`, `Audited Code SHA-256`, every named layout-affecting
   evidence field above, the four Scene commands in order, each exit code, and
   complete unedited output.
   Route every blocking finding to Stage 4 `SCENE_IMPLEMENTATION` / `CODE_PREPARATION` for correction.

## Completion criteria

`Result: PASS` is allowed only when preflight passed, all named environment
evidence fields are present, exactly four approved Scenes were audited, and
every required warning-level command exited `0`. Any missing input or named
environment field, command failure, warning, unverified code identity, or
inability to audit all four Scenes is `Result: FAIL`.

## Final response

- `DONE`: give the absolute `layout_audit_result.md` path, its `PASS` or `FAIL`
  result, the audited code SHA-256, and the four Scene exit codes.
- `BLOCKED`: use only when the environment prevents even writing
  `layout_audit_result.md`; give the evidence, affected absolute paths, and the
  action required from the coordinator.
