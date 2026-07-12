# Remove Pre-build Brief Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove the `CONTRACT` substage and `pre_build_brief.md` data path so every downstream stage consumes confirmed requirements and the approved animation design directly.

**Architecture:** `confirmed_requirements.md` remains the authority for user-supplied requirements, while `animation_design.md` remains the authority for the six-scene design. Script, voiceover, render, QA, and delivery consume those sources directly; narration is always required because requirement collection already mandates a narration language.

**Tech Stack:** Markdown workflow contracts, agent role definitions, ripgrep, Git diff checks

---

## File Structure

- Delete: `references/pre-build-brief.md` — remove the redundant summary contract.
- Modify: `SKILL.md` — remove `CONTRACT`, brief gates, delivery-tier branches, and no-narration paths.
- Modify: `agents/script-writer.md`, `agents/script-reviewer.md` — consume requirements and design directly.
- Modify: `agents/voiceover-manifest.md` — always produce the required narration package.
- Modify: `agents/scene-writer.md`, `agents/scene-reviewer.md`, `agents/qa-verifier.md`, `agents/layout-checker.md` — remove brief and delivery-tier routing.
- Modify: `references/teaching-script.md`, `references/script-review-checklist.md`, `references/voiceover.md` — define script and narration inputs without a brief.
- Modify: `references/manim-guidelines.md`, `references/how-to-hand-off-a-render-for-review.md`, `references/how-to-review-manim-scene-code.md`, `references/render-qa-checklist.md`, `references/default-visual-semantics.md` — update render and QA contracts.
- Modify: `references/how-to-design-animation.md` — transition directly from approved design to `SCRIPT`.
- Modify where applicable: current uncommitted workflow rewrite specs/plans — remove statements that describe the obsolete target workflow, while retaining historical committed documents that only record earlier decisions.

The target files already contain unrelated uncommitted changes. Implementation must preserve those changes and must not create an implementation commit that would accidentally include them.

### Task 1: Make ANIMATION_DESIGN transition directly to SCRIPT

**Files:**
- Modify: `SKILL.md:36-139`
- Modify: `references/how-to-design-animation.md:123-130`
- Delete: `references/pre-build-brief.md`

- [x] **Step 1: Capture the failing workflow references**

Run:

```bash
rg -n "pre_build_brief|pre-build-brief|\\bCONTRACT\\b" SKILL.md references/how-to-design-animation.md references/pre-build-brief.md
```

Expected: matches identify the substage, required artifact, gates, and return paths that must disappear.

- [x] **Step 2: Remove the CONTRACT substage and artifact**

Update `SKILL.md` so `ANIMATION_DESIGN` ends after:

```text
confirmed_requirements.md exists
animation_design.md contains six complete Scenes
animation_design_review.md = PASS
the user explicitly approved animation_design.md
```

Change the successful transition to `SCRIPT`. Remove `pre_build_brief.md` from required outputs, completion checks, invalidation rules, and failure routing. Delete `references/pre-build-brief.md`.

- [x] **Step 3: Update the design guide handoff**

Replace the final `CONTRACT` transition in `references/how-to-design-animation.md` with a direct transition to `SCRIPT` after independent review and explicit user approval.

- [x] **Step 4: Verify the first-stage workflow**

Run:

```bash
rg -n "pre_build_brief|pre-build-brief|\\bCONTRACT\\b" SKILL.md references/how-to-design-animation.md
test ! -e references/pre-build-brief.md
```

Expected: `rg` returns no matches and the file absence check exits 0.

### Task 2: Route SCRIPT through requirements and approved design

**Files:**
- Modify: `SKILL.md:109-139`
- Modify: `agents/script-writer.md`
- Modify: `agents/script-reviewer.md`
- Modify: `references/teaching-script.md`
- Modify: `references/script-review-checklist.md`

- [x] **Step 1: Replace brief inputs**

Require script writer and reviewer to read:

```text
confirmed_requirements.md
approved animation_design.md
teaching_script.md (reviewer only)
the applicable script reference/checklist
```

Define contract fidelity as fidelity to confirmed requirements and approved design. Remove `Delivery tier`, `Overlay Policy`, brief wording failures, and `CONTRACT` repair routes.

- [x] **Step 2: Preserve stage ownership**

Keep these return rules:

- Script wording, ordering, or beat-structure problems return to `SCRIPT`.
- Incorrectly captured user requirements return to `COLLECT_REQUIREMENTS`.
- Algorithm behavior, teaching presentation, Scene structure, or animation-design gaps return to `DESIGN_DEVELOPMENT` and require review plus user reapproval.

- [x] **Step 3: Verify SCRIPT references**

Run:

```bash
rg -n -i "pre_build_brief|\\bCONTRACT\\b|delivery tier|delivery-tier|overlay policy" agents/script-writer.md agents/script-reviewer.md references/teaching-script.md references/script-review-checklist.md
rg -n "confirmed_requirements\\.md|animation_design\\.md" agents/script-writer.md agents/script-reviewer.md references/teaching-script.md references/script-review-checklist.md
```

Expected: the first command has no matches; the second shows both authoritative inputs in the writer and reviewer contracts.

### Task 3: Make narration unconditional

**Files:**
- Modify: `SKILL.md:141-180`
- Modify: `agents/voiceover-manifest.md`
- Modify: `references/voiceover.md`

- [x] **Step 1: Remove delivery-tier branching**

Replace conditional narration behavior with one required path that produces:

```text
voiceover.md
narration_manifest.json
audio/voiceover/ usable narration audio
```

The narration language comes from `confirmed_requirements.md`. Remove English fallback behavior because requirement collection cannot complete without a confirmed narration language.

- [x] **Step 2: Define voiceover inputs and returns**

Require `confirmed_requirements.md`, approved `animation_design.md`, `teaching_script.md`, and `script_review_result.md`. Keep wording and pacing fixes in `VOICEOVER`; return beat-structure problems to `SCRIPT`, requirement-source problems to `COLLECT_REQUIREMENTS`, and design gaps to `DESIGN_DEVELOPMENT`.

- [x] **Step 3: Verify narration rules**

Run:

```bash
rg -n -i "pre_build_brief|\\bCONTRACT\\b|no narration|no-narration|delivery tier|delivery-tier|English" SKILL.md agents/voiceover-manifest.md references/voiceover.md
rg -n "voiceover\\.md|narration_manifest\\.json|audio/voiceover|confirmed_requirements\\.md" SKILL.md agents/voiceover-manifest.md references/voiceover.md
```

Expected: the first command has no matches; the second confirms all required narration artifacts and the language source.

### Task 4: Update render, scene review, QA, and delivery

**Files:**
- Modify: `SKILL.md:182-364`
- Modify: `agents/layout-checker.md`
- Modify: `agents/scene-writer.md`
- Modify: `agents/scene-reviewer.md`
- Modify: `agents/qa-verifier.md`
- Modify: `references/default-visual-semantics.md`
- Modify: `references/manim-guidelines.md`
- Modify: `references/how-to-hand-off-a-render-for-review.md`
- Modify: `references/how-to-review-manim-scene-code.md`
- Modify: `references/render-qa-checklist.md`

- [x] **Step 1: Replace render and review inputs**

Require render and QA roles to use:

```text
confirmed_requirements.md
approved animation_design.md
reviewed teaching_script.md
voiceover.md
narration_manifest.json
audio/voiceover/
latest render evidence
```

Keep `contract mismatch` only where it means conflict with approved design or reviewed script, or rename it to `source mismatch` when that is clearer. Remove `CONTRACT` as a repair destination.

- [x] **Step 2: Simplify review invalidation rules**

Full review remains required when a fix changes approved semantics, script beat order, whole-scene structure, whole-scene layout, render mapping, or invalidates affected-frame evidence. Remove delivery-tier and brief-specific conditions.

- [x] **Step 3: Simplify QA and delivery gates**

Require narration assets unconditionally. Validate narration language against `confirmed_requirements.md`. Delivery summaries describe actual artifacts and passed gates without referring to a delivery tier or brief.

- [x] **Step 4: Verify downstream references**

Run:

```bash
rg -n -i "pre_build_brief|pre-build brief|\\bCONTRACT\\b|no narration|no-narration|delivery tier|delivery-tier|交付層級|PRE_BUILD_BRIEF" agents references --glob '*.md'
```

Expected: no matches.

### Task 5: Repository-wide consistency verification

**Files:**
- Verify: `SKILL.md`
- Verify: `agents/*.md`
- Verify: `references/*.md`
- Update only if they describe the current target state: uncommitted `docs/superpowers/specs/*.md` and `docs/superpowers/plans/*.md`

- [x] **Step 1: Check obsolete workflow vocabulary**

Run:

```bash
rg -n -i "pre_build_brief|pre-build brief|pre-build-brief|\\bCONTRACT\\b|no narration|no-narration|delivery tier|delivery-tier|交付層級|PRE_BUILD_BRIEF" SKILL.md agents references --glob '*.md'
```

Expected: no matches.

- [x] **Step 2: Check required direct inputs**

Run:

```bash
rg -n "confirmed_requirements\\.md|animation_design\\.md|teaching_script\\.md|voiceover\\.md|narration_manifest\\.json" SKILL.md agents references --glob '*.md'
```

Expected: each stage and role lists the inputs it actually needs; no downstream role relies on an unnamed summary artifact.

- [x] **Step 3: Check the retained approval gates**

Run:

```bash
rg -n "animation_design_review\\.md = PASS|明確核准|獨立.*審查" SKILL.md references/how-to-design-animation.md agents/animation-design-reviewer.md
```

Expected: independent design review and explicit user approval remain mandatory before `SCRIPT`.

- [x] **Step 4: Check formatting and inspect the complete diff**

Run:

```bash
git diff --check
git diff --stat
git diff -- SKILL.md agents references docs/superpowers/specs docs/superpowers/plans
```

Expected: `git diff --check` has no output. The diff contains only the already-present workflow rewrite plus the approved removal, with no unrelated files changed by this implementation.

- [x] **Step 5: Do not commit overlapping implementation files automatically**

Because the target files had pre-existing uncommitted edits before this plan, leave the implementation diff unstaged for user review. A later commit may be created only after the user confirms the combined scope.
