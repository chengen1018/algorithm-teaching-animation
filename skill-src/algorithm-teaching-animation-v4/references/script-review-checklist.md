# Script Review Checklist

## Required Output
Return `script_review_result.md` with:

- `PASS` or `FAIL`
- independent reviewer authorship of the review result
- evidence-backed findings
- repair direction: `SCRIPT`, `DESIGN_DEVELOPMENT`, or `CONTRACT`

`script_review_result.md` must be authored by an independent reviewer. Self-review by the script writer is invalid.

## Review Inputs
- approved `pre_build_brief.md`
- `teaching_script.md`

## Review Questions
### Contract Fidelity

- Does the script stay inside the approved `pre_build_brief.md` rather than inventing new semantics?
- Do the beats honor the frozen `Resolved High-Impact Clarifications`, `Overlay Policy`, and `Delivery Tier`?
- Does any wording hide a fork that should have been frozen in the brief instead of guessed in the script?

Return to `DESIGN_DEVELOPMENT` when the script can only proceed because the approved design itself lacks or conflicts on algorithm semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, high-level beats, the delivery decision, or a newly surfaced high-impact fork. Require design repair, review, and reapproval, then brief regeneration and reapproval.
Return to `CONTRACT` when the approved design is clear but the script exposes wrong brief wording or source labels, or another failure of faithful conversion. Repair and reapprove the brief without redesign.

### Teaching Coherence

- Does each beat have one clear teaching purpose instead of mixed or drifting goals?
- Is the viewer's attention directed to the structure or action that matters most in that moment?
- Do progress cues accumulate into a legible lesson arc rather than isolated local descriptions?

Keep repair in `SCRIPT` when the teaching logic is present in the brief but the script explains it weakly or in the wrong order.

### Beat Completeness

- Does every beat define a viewer goal, algorithm moment, visual focus, teaching note, progress cue, and voiceover intent?
- Are support structures, pointers, boundaries, and temporary slots named clearly when the brief says they matter?
- Can a downstream scene writer implement the beat sequence without guessing what changed or why it matters?

Keep repair in `SCRIPT` when the script is structurally thin, missing beat fields, or too generic to drive render work.

### Beat Atomicity and Narration Readiness

- Does each beat contain a single teachable local event rather than several sequential local decisions that would need separate spoken timing?
- Can downstream voiceover stay beat-faithful without chasing multiple distinct local comparisons, swaps, or pointer moves inside one beat?
- Can a downstream scene writer implement the beat timing without inventing hidden sub-beats or deciding new emphasis locally?

Keep repair in `SCRIPT` when the brief is clear but the beat is too coarse for faithful synchronized narration.

### Voiceover Readiness

- Can `voiceover.md` stay beat-faithful to this script without inventing new teaching logic?
- Does each beat already contain the spoken takeaway the later narration should compress and naturalize?
- Would a voiceover writer need to resolve ambiguity about timing, emphasis, or semantic meaning that should already be explicit here?

Keep repair in `SCRIPT` when the script contains the right semantics but does not yet support faithful narration drafting.
Return to `DESIGN_DEVELOPMENT` when voiceover readiness fails because the approved design itself lacks or conflicts on the needed teaching or delivery decision. Require design repair, review, and reapproval, then brief regeneration and reapproval.
Return to `CONTRACT` when the approved design clearly fixes the needed teaching or delivery decision but the brief mistranslated it. Repair and reapprove the brief without redesign.

## Repair Routing

### Stay Within SCRIPT

Use this when the approved brief is clear and the problem is limited to:

- weak beat structure
- missing progress cues
- vague viewer goals
- unclear voiceover intent
- beat sizing that forces one narration segment to step through multiple distinct local state transitions
- ordering or emphasis problems that do not change frozen semantics

### Return to DESIGN_DEVELOPMENT

Use this when the failure exposes:

- the approved design itself lacks or conflicts on algorithm semantics
- the approved design itself lacks or conflicts on the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, or high-level beats
- the approved design itself lacks or conflicts on the delivery decision
- the approved design itself lacks or conflicts on a newly surfaced high-impact fork

Require design repair, review, and reapproval, then brief regeneration and reapproval.

### Return to CONTRACT

Use this when the approved design is clear but `pre_build_brief.md` has wrong wording or source labels, or otherwise failed faithful conversion. Repair and reapprove the brief without redesign.

## PASS Standard
- the script matches the approved brief
- every beat has a concrete teaching purpose
- no unresolved semantic ambiguity remains hidden in the script
- downstream voiceover and render work can proceed without guessing
- `script_review_result.md` is written by an independent reviewer rather than the script writer

## Common Failures
- generic beat prose that could fit multiple conflicting semantics
- missing progress cues or viewer goals
- script structure that forces voiceover to invent new teaching logic
- beat structure that forces downstream phases to infer hidden sub-beat timing or treat beat oversizing as a voiceover or render convenience issue
- brief ambiguities patched inside the script instead of escalated
