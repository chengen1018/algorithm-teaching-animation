# Teaching Script

This document defines `teaching_script.md` in `algorithm-teaching-animation-v3`.

The script is the teaching-structure layer between the confirmed brief and the final scene.

It is not:

- a replacement for clarification
- a place to settle unresolved semantics
- a line-by-line scene implementation

## Purpose

The script should translate the frozen brief into a beat sequence that answers:

- what each beat is trying to teach
- what the viewer should inspect
- how local actions build toward the overall lesson

## Source of Truth

The script must be derived from:

- approved `pre_build_brief.md`
- the concrete sample input or scenario
- code or pseudocode only when needed to stay faithful to the algorithm flow

If the script needs a semantic choice because the approved design itself lacks or conflicts on algorithm semantics, the primary mental model, core visual semantics, scene structure, information hierarchy, teaching arc, high-level beats, the delivery decision, or a newly surfaced high-impact fork, stop and return to `DESIGN_DEVELOPMENT`; require design repair, review, and reapproval, then brief regeneration and reapproval.

If the approved design is clear but the brief has wrong wording or source labels, or otherwise failed faithful conversion, stop and return to `CONTRACT` for brief repair and reapproval without redesign.

## Gate Dependency

`teaching_script.md` is not approved for downstream narration or render work until an independent review returns `script_review_result.md = PASS`.

No narration work may begin before script review passes.

## Recommended Structure

```md
# Teaching Script

## Summary
- Algorithm:
- Teaching goal:
- Audience:
- Delivery tier:
- Key semantics:

## Beats

### Beat 1: ...
- Viewer goal:
- Algorithm moment:
- Visual focus:
- Teaching note:
- Progress cue:
- Voiceover intent:

### Beat 2: ...
...
```

The exact headings may vary, but the information should remain easy to audit.

## Required Beat Content

Each beat should define:

- `Viewer goal`: what the viewer should understand from this beat
- `Algorithm moment`: the part of the algorithm flow this beat covers
- `Visual focus`: what should receive the strongest attention
- `Teaching note`: why this moment matters
- `Progress cue`: what remains true after the beat
- `Voiceover intent`: the spoken takeaway the later voiceover should carry

## Script Rules

- one beat should have one main teaching point and one primary local teaching event
- use concrete viewer-facing language
- keep beat order faithful to the frozen semantics
- keep support structures visible in beats where they matter to the lesson
- do not hide unresolved ambiguity under generic wording such as "the normal step"
- do not pack multiple named local comparisons, selections, swaps, or pointer moves into one beat when they require separate spoken attention

## Beat Design Guidance

Good beats usually follow this rhythm:

1. establish the current local state
2. show the local decision or transformation
3. expose the progress cue or invariant

The beat can be longer or shorter than one loop iteration, but it should stay teachable.

## Beat Atomicity Guidance

For narrated tiers, a beat should usually correspond to one teachable unit that can stay visually coherent under one voiceover segment.

Use a finer beat split when the viewer needs to track multiple local decisions in sequence, especially for moments such as:

- compare-then-choose between two active candidates
- swap or pointer move that changes the local state
- re-test of the moved candidate at a new location

If the spoken explanation would need to say "then ... then ... then ..." across multiple local comparisons, swaps, or pointer moves, the beat is usually too coarse and should be split upstream in `SCRIPT`.

A beat may summarize repeated work only when the teaching goal is explicitly summary-level rather than step-by-step understanding.

## Relationship to Voiceover

The script is the upstream teaching source for beat-faithful voiceover derived from the approved script.

That means:

- the script should already contain the teaching logic
- the later voiceover should compress and naturalize it without changing beat meaning
- if the voiceover needs to invent a new idea, the script is incomplete

## Script Review Handoff

The script must be reviewable against the approved brief before any narration or scene phase treats it as settled.

The review gate result is `script_review_result.md`.

Use that review to confirm:

- the script matches the approved brief
- every beat has a concrete teaching purpose
- downstream voiceover can stay beat-faithful without guessing
- downstream render work does not need to invent missing semantics

## Relationship to Scene Work

The script should be strong enough that a scene writer can implement it without guessing:

- where the focus should land
- which structure must remain visible
- when progress should become visible

The scene may choose layout details, but it should not have to choose the lesson.

## Common Failures

- Writing a scene description instead of a teaching plan.
- Writing generic algorithm prose that does not map to beats.
- Packing multiple unrelated takeaways into one beat.
- Packing several sequential local decisions into one beat and expecting downstream voiceover or scene work to infer hidden sub-beat timing.
- Letting script structure drift away from the frozen brief.
