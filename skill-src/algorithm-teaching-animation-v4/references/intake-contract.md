# Intake Contract

Use this reference to normalize a minimal request into the formal `intake_summary.md` artifact without freezing later design choices.

INTAKE records and classifies the request. It does not perform complete animation design. Core visual semantics, scene structure, persistent support structures, information hierarchy, teaching progression, and high-level beats belong to `animation-designer` in `DESIGN_DEVELOPMENT`.

## Minimum Expected Input

Start intake as soon as you have:

- algorithm name
- sample input or target scenario
- special animation preference, if any

Useful optional inputs:

- audience notes
- desired delivery tier
- pseudocode or implementation code
- known semantic preferences
- explicit overlay requests

## Intake Summary Schema

Produce `intake_summary.md` in this shape:

```md
# Intake Summary

- Algorithm:
- Sample input / scenario:
- Explicit user requests (source: user):
- Constraints and prohibitions (source: user):
- Support classification: first-class / best-effort
- Classification rationale:
- Candidate teaching framing:
- Suggested delivery tier:
- Likely high-impact gaps:
```

Preserve source wording for requirements, constraints, prohibitions, and prior decisions that could affect semantics, teaching, delivery, or acceptance. Label direct user statements as user-sourced; label derived classification, candidate framing, and suggestions as agent analysis. Do not rewrite an agent inference as a user requirement.

Keep `Candidate teaching framing` lightweight:

- a `primary framing`
- an optional `secondary framing`
- a short note about why that framing matches the user goal
- the semantic or teaching-focus areas most likely to matter in clarification

## Classification Rules

### First-Class Support

Treat these as first-class support:

- array sorting
- binary search and interval or candidate-region narrowing two-pointer searches only
- basic graph traversal such as BFS or DFS

### Best-Effort Support

Treat categories such as these as best-effort unless the skill adds stronger local guidance:

- dynamic programming table construction
- tree transformations
- greedy or interval algorithms
- specialized graph algorithms

Record best-effort status and its rationale in `intake_summary.md`; it must remain visible in later design risks and brief notes.

Broad two-pointer requests and non-elimination searches are not first-class merely because they use pointers or contain the word "search." Use a matching specialized design reference when one is available. Otherwise route them through the common design guidance, classify them as best-effort, disclose the specific coverage risk, and require the strengthened independent review defined by `animation-design-review-checklist.md`.

## Candidate Teaching Framing

Intake may suggest a likely framing, but candidate framing is non-binding and must not lock semantics, teaching focus, scene structure, or visual choices.

Common framings:

- algorithm walkthrough
- pointer and boundary explainer
- graph traversal explainer
- state-construction explainer
- comparison or intuition explainer

If multiple framings are plausible, carry the ambiguity forward instead of collapsing it early. Route any unresolved choice that could affect the core design to `animation-designer` in `DESIGN_DEVELOPMENT`.

## Intake Rules

- Preserve user wording for special requests.
- Preserve source labels and distinguish user wording from agent classification or suggestions.
- Do not spend intake budget on low-value styling questions.
- Do not require code when the algorithm and scenario are already clear.
- Do not silently infer final semantics from code unless the user wants code-faithful behavior.
- Do not let one flashy request distort the main teaching target.
- Do not settle unresolved design choices or produce a complete animation design during INTAKE.

## When to Use Code or Pseudocode

Use code or pseudocode to:

- confirm control flow
- resolve implementation-specific branches after code fidelity is made relevant
- disambiguate edge cases that affect the lesson

Do not use code or pseudocode to:

- bypass clarification
- override an explicit teaching preference
- force a concept-first request into a code-first explanation

## Escalation Examples

- If the sample input is missing and the algorithm depends on visible ordering or structure shape, flag the missing scenario for clarification.
- If the user's concept goal and supplied code imply different semantics, preserve both signals and escalate the conflict instead of choosing one.
- If two teaching framings would lead to different beat emphasis, record both as non-binding candidates and route the choice to `DESIGN_DEVELOPMENT`.

## Common Failures

- Refusing to start because the user did not provide code.
- Treating a concrete sample scenario as optional when the lesson depends on it.
- Converting a candidate teaching framing into a settled semantic decision.
- Losing explicit user requests while summarizing the intake.
- Omitting support classification or hiding that a category is best-effort.
- Designing core visual semantics, scene structure, or high-level beats during INTAKE.
