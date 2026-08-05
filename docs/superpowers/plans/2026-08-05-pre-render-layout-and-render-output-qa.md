# Pre-render Layout and Render Output QA Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the Manim algorithm animation skill so layout validation happens before rendering, rendered-media validation happens after rendering, and each agent has a non-overlapping, hash-bound contract.

**Architecture:** Keep the existing five-stage workflow, but replace Stage 4 with `SCENE_IMPLEMENTATION` and Stage 5 with `FINAL_RENDER_AND_QA`. `scene_writer` produces code, `scene_layout_validator` performs deterministic non-rendering geometry checks, `scene_reviewer` checks semantic fidelity and lifecycle, and `rendered_media_validator` checks the final MP4/audio artifacts. Every gate records the `generated_algo_scene.py` SHA-256; code or layout-affecting environment changes invalidate downstream evidence.

**Tech Stack:** Markdown skill/reference files, YAML metadata, Python Manim dry-run runner, `ffprobe`/`ffmpeg` media inspection, shell-based documentation checks, and the skill creator `quick_validate.py` validator.

## Global Constraints

- Preserve the five stages: `ANIMATION_DESIGN`, `SCRIPT`, `VOICEOVER`, `SCENE_IMPLEMENTATION`, `FINAL_RENDER_AND_QA`.
- `scene_layout_validator` runs all four Scene dry-runs before any formal Manim render.
- `scene_reviewer` owns source fidelity, algorithm/state correctness, lifecycle, cleanup, and assumptions; it does not duplicate bounding-box judgment.
- `rendered_media_validator` owns post-render MP4/audio/metadata/duration/order/hash checks; it does not modify code or media.
- Formal render may use only the code version for which handoff, layout, and scene review hashes all match and are `PASS`.
- Any `generated_algo_scene.py` change invalidates handoff, layout result, scene review, render manifest, and rendered-media validation.
- Layout runner, Manim version, font, frame geometry, or other layout-affecting environment changes invalidate layout-dependent evidence.
- Preserve the user’s existing uncommitted work; do not reset, checkout, or stage unrelated files.
- Execute from an isolated worktree or a clean baseline commit that contains the user’s intended current refactor; if that baseline is unavailable, stop before editing overlapping files.
- Do not rewrite the layout algorithm or introduce an unrelated media framework; document the existing runner and standard media tools.

## File Map

### Files to modify

- `manim-algorithm-animation-maker/SKILL.md` — replace the current Stage 4/5 workflow, gates, outputs, and invalidation rules.
- `manim-algorithm-animation-maker/references/subagent-delegation-protocol.md` — rename the layout task and add the rendered-media task mapping.
- `manim-algorithm-animation-maker/references/subagent-scene-writer.md` — define `CODE_PREPARATION` and `FINAL_RENDER` responsibilities under the new stage names.
- `manim-algorithm-animation-maker/references/subagent-scene-reviewer.md` — narrow review scope to semantic contract, state/lifecycle, assumptions, and audit evidence.
- `manim-algorithm-animation-maker/references/how-to-hand-off-scene-code-for-review.md` — keep handoff pre-render and require the source hash/environment evidence used by both validators.
- `manim-algorithm-animation-maker/references/how-to-review-manim-scene-code.md` — remove duplicate geometry authority while retaining static lifecycle and source-fidelity checks.
- `manim-algorithm-animation-maker/references/layout-audit.md` — describe the runner as Stage 4 pre-render validation and keep its warning/adapter rules explicit.
- `manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md` — require Stage 4’s dual PASS, emit a hash-rich render manifest, and route code changes back to Stage 4.
- `manim-algorithm-animation-maker/agents/openai.yaml` — update the skill’s short UI description only if it is stale relative to the new pre-render/post-render workflow; there are no role-specific entries to duplicate.

### Files to create or rename

- Rename/create `manim-algorithm-animation-maker/references/subagent-scene-layout-validator.md` from the current layout-auditor contract.
- Create `manim-algorithm-animation-maker/references/subagent-rendered-media-validator.md` for post-render artifact QA.
- Do not recreate deleted `.codex/agents/*.toml` files; the current migration uses reference-based subagent contracts.

### Files used for validation, not modified by this plan

- `manim-algorithm-animation-maker/scripts/run_layout_audit.py`
- `manim-algorithm-animation-maker/scripts/visible_layout_audit.py`
- `manim-algorithm-animation-maker/scripts/scene_layout_audit.py`
- `docs/superpowers/specs/2026-08-05-pre-render-layout-and-render-output-qa-design.md`

---

### Task 1: Establish the renamed validator contracts

**Files:**
- Create: `manim-algorithm-animation-maker/references/subagent-scene-layout-validator.md`
- Create: `manim-algorithm-animation-maker/references/subagent-rendered-media-validator.md`
- Modify: `manim-algorithm-animation-maker/references/subagent-delegation-protocol.md`
- Remove after migration: `manim-algorithm-animation-maker/references/subagent-layout-auditor.md`

**Interfaces:**
- `scene_layout_validator` consumes `generated_algo_scene.py`, `scene_code_review_handoff.md`, `layout-audit.md`, and `run_layout_audit.py`; it produces `layout_audit_result.md` with `Result`, `Audited Code SHA-256`, runner/environment metadata, four Scene commands, exit codes, and complete output.
- `rendered_media_validator` consumes the approved source/gate files, `render_manifest.md`, `narration_manifest.json`, four Scene MP4s, and the combined MP4; it produces `rendered_media_validation_result.md` with media commands, exit codes, metadata, hashes, duration/audio/order checks, and `PASS`/`FAIL`.
- Delegation protocol maps task names exactly to `scene_layout_validator` and `rendered_media_validator`.

- [ ] **Step 1: Write the failing contract checks**

Create a temporary shell check in the command line (do not add a permanent test file) that asserts the new task names and required output names are present. Before editing, run:

```bash
rg -n "layout_auditor|render_output_auditor|scene_layout_validator|rendered_media_validator" \
  manim-algorithm-animation-maker/references
```

Expected: the old contract is present, and the new contracts are absent.

- [ ] **Step 2: Write the minimal role contracts**

Write the two role files with: role boundary, absolute-path input requirements, preflight, forbidden actions, exact procedure, completion criteria, and `DONE`/`BLOCKED` response shape. The layout role must explicitly forbid formal render; the media role must explicitly forbid modifying or re-encoding artifacts.

For media verification, document these concrete checks rather than vague “validate output” language:

```bash
ffprobe -v error -show_format -show_streams -of json <file.mp4>
ffmpeg -v error -i <file.mp4> -f null -
sha256sum <file.mp4>
```

- [ ] **Step 3: Update the delegation map and remove the obsolete contract**

Replace the old row with:

```markdown
| 渲染前 Scene 版面驗證 | `scene_layout_validator` | `references/subagent-scene-layout-validator.md` |
| 渲染後媒體成品驗證 | `rendered_media_validator` | `references/subagent-rendered-media-validator.md` |
```

Remove the obsolete role file only after every active reference points to the renamed path.

- [ ] **Step 4: Run contract checks**

Run:

```bash
! rg -n "task name.*layout_auditor|task name.*render_output_auditor|subagent-layout-auditor" \
  manim-algorithm-animation-maker/SKILL.md \
  manim-algorithm-animation-maker/references
rg -n "scene_layout_validator|rendered_media_validator|layout_audit_result.md|rendered_media_validation_result.md" \
  manim-algorithm-animation-maker/references
```

Expected: the negative check succeeds; the positive check finds both contracts and the delegation rows.

- [ ] **Step 5: Commit**

```bash
git add manim-algorithm-animation-maker/references
git commit -m "docs: define scene and media validator contracts"
```

### Task 2: Separate scene-writer and scene-reviewer responsibilities

**Files:**
- Modify: `manim-algorithm-animation-maker/references/subagent-scene-writer.md`
- Modify: `manim-algorithm-animation-maker/references/subagent-scene-reviewer.md`
- Modify: `manim-algorithm-animation-maker/references/how-to-hand-off-scene-code-for-review.md`
- Modify: `manim-algorithm-animation-maker/references/how-to-review-manim-scene-code.md`

**Interfaces:**
- Writer mode `CODE_PREPARATION` produces only `generated_algo_scene.py` and `scene_code_review_handoff.md`; it performs self-checks but no formal render.
- Writer mode `FINAL_RENDER` consumes Stage 4 PASS evidence and produces the four Scene MP4s, combined MP4, and `render_manifest.md`; any code fix returns `BLOCKED` to Stage 4.
- Reviewer consumes upstream contract files plus `layout_audit_result.md`; it produces `scene_review_result.md` and records `Reviewed Code SHA-256` plus the layout-audited hash.

- [ ] **Step 1: Write the failing responsibility checks**

Run:

```bash
rg -n "static layout risk|bounding|layout|MP4|render" \
  manim-algorithm-animation-maker/references/subagent-scene-reviewer.md \
  manim-algorithm-animation-maker/references/how-to-review-manim-scene-code.md
```

Expected baseline: the reviewer contract still treats static layout risk as a review category and does not require the pre-render layout result.

- [ ] **Step 2: Rewrite the writer contract**

Keep the existing upstream preflight, but split the procedure into `CODE_PREPARATION` and `FINAL_RENDER`. In `CODE_PREPARATION`, require full-file reread, static self-audit, handoff creation, and `Manim render performed: NO`. In `FINAL_RENDER`, require all Stage 4 hashes to match before rendering and forbid code edits after the gate.

- [ ] **Step 3: Narrow the reviewer contract**

Retain implementation fidelity, algorithm/state correctness, lifecycle/ownership, cleanup, and assumptions. Remove reviewer authority over actual mobject geometry. Require the reviewer to verify that `layout_audit_result.md = PASS`, covers all four Scenes, and matches the reviewed code hash.

- [ ] **Step 4: Update handoff and checklist evidence**

Make `scene_code_review_handoff.md` explicitly pre-render. Make `scene_review_result.md` record both reviewed code hash and the layout-audited hash. Preserve the rule that reviewer never edits code or render artifacts.

- [ ] **Step 5: Run reviewer/writer checks**

```bash
rg -n "CODE_PREPARATION|FINAL_RENDER|Manim render performed: NO|Reviewed Code SHA-256|layout_audit_result.md" \
  manim-algorithm-animation-maker/references/subagent-scene-writer.md \
  manim-algorithm-animation-maker/references/subagent-scene-reviewer.md \
  manim-algorithm-animation-maker/references/how-to-hand-off-scene-code-for-review.md \
  manim-algorithm-animation-maker/references/how-to-review-manim-scene-code.md
! rg -n "scene-reviewer.*static layout risk|reviewer.*bounding-box.*PASS" \
  manim-algorithm-animation-maker/references/subagent-scene-reviewer.md
```

Expected: both writer modes and hash evidence are present; the reviewer contract contains no duplicate geometry authority.

- [ ] **Step 6: Commit**

```bash
git add manim-algorithm-animation-maker/references
git commit -m "docs: separate scene review from layout validation"
```

### Task 3: Move layout validation into the Stage 4 pre-render gate

**Files:**
- Modify: `manim-algorithm-animation-maker/SKILL.md`
- Modify: `manim-algorithm-animation-maker/references/layout-audit.md`

**Interfaces:**
- Stage 4 sequence is `scene_writer CODE_PREPARATION → scene_layout_validator → scene_reviewer → hash-bound pre-render gate`.
- Stage 4 outputs are `generated_algo_scene.py`, `scene_code_review_handoff.md`, `layout_audit_result.md`, and `scene_review_result.md`; no current-version MP4 is required or accepted.
- Stage 5 cannot start unless all four Scene layout audits and the scene review are `PASS` for the current source hash.

- [ ] **Step 1: Write the failing order check**

Run:

```bash
python -c 'from pathlib import Path; t=Path("manim-algorithm-animation-maker/SKILL.md").read_text(); assert t.index("layout_auditor") < t.index("## 階段 5")'
rg -n "## 階段 4|## 階段 5|layout_audit_result|FINAL_RENDER|QA.*渲染" \
  manim-algorithm-animation-maker/SKILL.md
```

Expected baseline: the layout validator is still described under the post-render QA section.

- [ ] **Step 2: Rewrite Stage 4 in the skill**

Add `SCENE_IMPLEMENTATION` with explicit Entry gate, `CODE_PREPARATION`, `LAYOUT_VERIFICATION`, `CONTRACT_REVIEW`, exit gate, outputs, and failure routing. Require the exact runner command for every Scene and bind all PASS files to one code hash.

- [ ] **Step 3: Rewrite Stage 5 in the skill**

Add `FINAL_RENDER_AND_QA` with `FINAL_RENDER` and `DELIVERY_QA`. Require the new rendered-media validator and post-render output checks. State that layout audit is not repeated in Stage 5.

- [ ] **Step 4: Update layout-audit reference timing**

Change “Use the audit runner during `QA`” to Stage 4 pre-render wording. Preserve the dry-run behavior, warning handling, scene-specific adapter rule, and limitation that between-endpoint animation artifacts are outside dry-run coverage.

- [ ] **Step 5: Add the invalidation matrix and completion checklist**

Document code hash, environment/profile, upstream-content, layout failure, reviewer failure, render-output, and media-output invalidation rules. Update the final checklist so Stage 4 requires both validator/reviewer PASS files and Stage 5 requires manifest plus rendered-media validation PASS.

- [ ] **Step 6: Run stage-order checks**

```bash
rg -n "SCENE_IMPLEMENTATION|FINAL_RENDER_AND_QA|scene_layout_validator|rendered_media_validator|layout_audit_result.md|rendered_media_validation_result.md" \
  manim-algorithm-animation-maker/SKILL.md
! rg -n "## 階段 5：QA|使用程式化 layout audit 檢查已渲染版本" \
  manim-algorithm-animation-maker/SKILL.md
```

Expected: the skill contains the new phase names and roles; Stage 5 no longer presents layout audit as a post-render check.

- [ ] **Step 7: Commit**

```bash
git add manim-algorithm-animation-maker/SKILL.md manim-algorithm-animation-maker/references/layout-audit.md
git commit -m "docs: gate layout validation before render"
```

### Task 4: Define final render and rendered-media QA evidence

**Files:**
- Modify: `manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md`
- Modify if stale: `manim-algorithm-animation-maker/agents/openai.yaml`

**Interfaces:**
- `render_manifest.md` binds approved code hash to four Scene MP4s and the combined MP4, including SHA-256 and media metadata.
- `rendered_media_validator` consumes the manifest and artifacts and writes `rendered_media_validation_result.md`.
- Output-only failures remain in Stage 5; any code change invalidates Stage 4.

- [ ] **Step 1: Write the failing manifest checks**

```bash
rg -n "Code SHA-256|MP4|Combined Output|Review status" \
  manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md
```

Expected baseline: the manifest does not require per-file SHA-256, media metadata, or a rendered-media validation result.

- [ ] **Step 2: Update render preflight and failure routing**

Require current code hash, handoff hash, layout hash, and reviewer hash to match before any render. Distinguish output-path/concat/metadata failures that can stay in Stage 5 from fixes requiring code changes that return to Stage 4.

- [ ] **Step 3: Expand the manifest contract**

Add render profile, Manim version, each Scene command, each MP4 SHA-256, size, mtime, duration, resolution, frame rate, audio stream data, concat order/command, and combined-file SHA-256/metadata.

- [ ] **Step 4: Update skill metadata only if needed**

If `agents/openai.yaml` still describes the skill without validation, update only `short_description` or `default_prompt` to mention complete pre-render and post-render verification. Do not add role-specific metadata that the file does not support.

- [ ] **Step 5: Run render-reference checks**

```bash
rg -n "layout_audit_result.md|rendered_media_validation_result.md|SHA-256|ffprobe|audio|duration|frame rate|concat" \
  manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md \
  manim-algorithm-animation-maker/references/subagent-rendered-media-validator.md
command -v ffprobe
command -v ffmpeg
```

Expected: all required evidence fields and media tools are documented and available.

- [ ] **Step 6: Commit**

```bash
git add manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md \
  manim-algorithm-animation-maker/agents/openai.yaml
git commit -m "docs: define rendered media delivery checks"
```

### Task 5: Run integrated skill validation and close documentation gaps

**Files:**
- Modify only files identified by the checks above.
- Test: the skill package and all active references.

**Interfaces:**
- The final package has no active references to the obsolete role/task names.
- The skill’s phase order, artifact names, and invalidation rules match the approved spec.
- Existing layout scripts remain executable and unchanged unless a test exposes a concrete incompatibility.

- [ ] **Step 1: Run structural validation**

```bash
python /Users/lichengen/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  manim-algorithm-animation-maker
```

Expected: frontmatter and skill naming validation pass.

- [ ] **Step 2: Run cross-reference checks**

```bash
! rg -n "layout_auditor|render_output_auditor|subagent-layout-auditor" \
  manim-algorithm-animation-maker
rg -n "scene_layout_validator|rendered_media_validator|SCENE_IMPLEMENTATION|FINAL_RENDER_AND_QA" \
  manim-algorithm-animation-maker
```

Expected: obsolete names are absent from active package files; new names and phase identifiers are present.

- [ ] **Step 3: Run formatting and consistency checks**

```bash
git diff --check
rg -n "TODO|TBD|FIXME" manim-algorithm-animation-maker docs/superpowers/plans/2026-08-05-pre-render-layout-and-render-output-qa.md
```

Expected: `git diff --check` passes; any match in the second command must be an intentional example or acceptance-criterion phrase, not an unresolved placeholder.

- [ ] **Step 4: Review the final diff against the approved spec**

Check each approved requirement: pre-render layout order, separated reviewer scope, exact new agent names, hash binding, Stage 5 media checks, and all recovery routes. Confirm no unrelated files or the user’s existing changes are staged.

- [ ] **Step 5: Commit the integrated documentation update**

```bash
git add \
  manim-algorithm-animation-maker/SKILL.md \
  manim-algorithm-animation-maker/agents/openai.yaml \
  manim-algorithm-animation-maker/references/subagent-delegation-protocol.md \
  manim-algorithm-animation-maker/references/subagent-scene-layout-validator.md \
  manim-algorithm-animation-maker/references/subagent-rendered-media-validator.md \
  manim-algorithm-animation-maker/references/subagent-scene-writer.md \
  manim-algorithm-animation-maker/references/subagent-scene-reviewer.md \
  manim-algorithm-animation-maker/references/how-to-hand-off-scene-code-for-review.md \
  manim-algorithm-animation-maker/references/how-to-review-manim-scene-code.md \
  manim-algorithm-animation-maker/references/layout-audit.md \
  manim-algorithm-animation-maker/references/how-to-render-approved-manim-scenes.md
git diff --cached --name-only
git commit -m "docs: complete five-stage render verification workflow"
```

Expected staged paths are limited to the files listed above; if any unrelated path appears, unstage it before committing.

## Final Verification Checklist

- [ ] `scene_layout_validator` runs before formal render and checks all four Scenes.
- [ ] `scene_reviewer` verifies semantic fidelity, state/lifecycle, assumptions, and audit evidence without owning geometry.
- [ ] `rendered_media_validator` checks every Scene MP4 and the combined MP4 after render.
- [ ] Handoff, layout result, scene review, render manifest, and rendered-media result all bind to the approved code hash where applicable.
- [ ] Code changes, layout-affecting environment changes, upstream changes, and output-only failures route to the correct stage.
- [ ] No obsolete agent names remain in active skill files.
- [ ] `quick_validate.py` and `git diff --check` pass.
- [ ] The final staged diff excludes the user’s unrelated worktree changes.
