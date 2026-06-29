# High-Impact Clarification

Use this reference as the high-impact question inventory for `animation-designer` during `DESIGN_DEVELOPMENT`. The inventory helps the designer find blocking core choices; clarification supports design and is not a substitute for producing `animation_design.md`.

## Batch Protocol

The designer plans a small internal batch of closely related blocking questions needed for the next design step. For every question, provide:

- a concrete recommendation;
- the rationale for that recommendation;
- the meaningful tradeoff or consequence;
- concise answer choices when useful.

The orchestrator asks exactly one user-facing question at a time, waits for the answer, and records it faithfully before asking the next planned question. It must not reinterpret, weaken, merge, or silently replace the user's answer with the recommendation.

After all questions in the planned batch have been answered, the orchestrator returns one consolidated batch of faithfully recorded answers to `animation-designer`. Do not return to the designer after each answer. The designer updates the design once and reassesses all remaining core gaps. Another small batch occurs whenever that reassessment finds any unresolved blocker, including a newly exposed blocker.

## What Counts as High Impact

A gap is high impact when the answer would change any of:

- animation semantics
- teaching focus
- delivery content

If the answer changes only ordinary styling or color, minor placement, a routine transition, easing, or local timing, it is not high impact unless the specific choice is explicitly important to accessibility, correctness, acceptance, or the teaching goal.

## Decision Classes

### Semantic Forks

Use this class when multiple reasonable interpretations exist and the choice changes what the viewer learns.

Examples:

- insertion sort movement model
- binary search interval convention
- whether graph traversal marks nodes on discovery or on processing

### Teaching-Focus Forks

Use this class when different emphases would change beat structure or visual attention.

Examples:

- binary search as interval reasoning versus branch-control reasoning
- BFS as queue behavior versus layer expansion
- sorting as movement intuition versus boundary progress

### Delivery-Affecting Forks

Use this class when the answer changes deliverable shape or layout obligations.

Examples:

- no narration versus final narrated delivery
- whether overlays are enabled
- whether a support structure must remain visibly present

## First-Class Support Inventories

Use these compact inventories when the intake category is first-class support.

### Array Sorting

Check at least:

- active comparison unit
- meaningful movement-semantics fork
- settled-progress expression
- whether a temporary holding position is part of the lesson

### Binary Search and Interval or Candidate-Region Narrowing Two-Pointer Search

Use this first-class inventory only for binary search and two-pointer searches that eliminate an interval or candidate region.

Check at least:

- interval convention
- pointer meaning
- stopping rule or success criterion
- whether the lesson emphasizes elimination logic, pointer choreography, or both

Broad or non-elimination two-pointer and search requests do not use this inventory automatically. Use a matching specialized reference when available; otherwise use the common design guidance, mark the request best-effort, disclose its coverage risk, and require strengthened independent review.

### BFS and DFS

Check at least:

- support-structure visibility
- visited timing
- discovery versus processing emphasis
- frontier or stack/path emphasis
- neighbor-order expectations when the sample input makes order visible

## What Not to Ask

Do not spend clarification budget on:

- ordinary color preferences
- minor pointer or label placement
- routine transitions
- easing
- local timing or pacing polish
- normal camera restraint choices
- subtitle requests unless the user actually wants overlays

These low-impact details belong to best-effort defaults and must not block `DESIGN_READY`. Ask one only when the intake or current design makes its impact explicit.

## Designer Inventory Result

The designer may organize its internal inventory in this shape before planning the next small batch:

```md
# High-Impact Inventory

## Resolved High-Impact Decisions
- Decision:
- Why it matters:
- Source: user answer / user-approved default

## Delivery Decisions
- Delivery tier:
- Overlay policy:

## Still Blocked
- None

## Low-Impact Defaults (Not Questions)
- Default:
- Why it is low risk:
```

## Proposed Default Rules

When proposing a default, phrase it as an explicit decision the user can approve or edit.

Good pattern:

- "If you do not have a preference, I will treat the active search interval as closed and keep eliminated regions dimmed."

Bad pattern:

- silently writing the interval rule into the brief
- asking a vague question with no explanation of why the choice matters

## Escalation Examples

- If intake suggested two plausible teaching framings and each would change beat emphasis, ask that teaching-focus fork directly instead of choosing one.
- If the user does not care about a high-impact semantic fork, offer a concrete default for approval rather than hiding it in the brief.
- If a delivery-tier change would also change overlays, narration, or support-structure visibility, freeze those decisions together.
- If reassessment after a completed batch exposes a new semantic, teaching, or delivery blocker, plan another small batch rather than guessing or declaring `DESIGN_READY`.

## Common Failures

- Asking low-value questions while missing the semantic fork that actually matters.
- Treating a delivery decision as optional when it changes layout or outputs.
- Writing "follow standard semantics" when multiple standards exist.
- Smuggling unresolved ambiguity into broad wording such as "show the normal process."
- Asking a batch as one multi-part user-facing question or returning answers to the designer one at a time.
- Omitting the recommendation, rationale, or tradeoff from a question.
