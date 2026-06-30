# Animation Design Process

## Purpose

Define the contract for DESIGN_DEVELOPMENT. Its primary job is to design how the animation teaches and presents the algorithm. Clarification supports that work; it is not a substitute for producing the design.

The process must produce an `animation_design.md` that is ready for explicit user confirmation and downstream review.

## Inputs

Use the approved task context, algorithm name and variant, sample input, audience and learning goals, animation requirements, relevant project contracts, and all user decisions already recorded.

Treat missing information according to impact. Ask only when an unresolved answer could materially change algorithm semantics, the primary mental model, the core visual metaphor, the teaching arc, or the high-level animation beats. Resolve lower-impact details with a documented best-effort choice.

## Design Responsibilities

DESIGN_DEVELOPMENT must actually design, not merely collect preferences or restate inputs. It owns:

- the primary mental model the viewer should build;
- the visual presentation, including metaphor, visual semantics, structure presentation, scene organization, and information hierarchy;
- the teaching arc from motivation and setup through state changes, insight, and conclusion;
- the high-level animation beats that make algorithm state and causality visible;
- a recommended design, relevant alternatives, and the tradeoffs that justify the recommendation;
- prevention of likely viewer misconceptions;
- faithful incorporation of confirmed user decisions and explicit notation of best-effort assumptions.

Every design choice must serve the stated audience and learning goal. Do not turn low-level implementation details into design requirements unless they affect what the viewer learns or sees.

## Core-Question Batch Protocol

The designer must identify unresolved core questions and plan a small question batch. A batch must contain only closely related decisions needed for the next design step; do not present a long questionnaire.

The orchestrator must ask exactly one user-facing question at a time, wait for its answer, and record that answer before asking the next planned question. Each question must include:

1. a concrete recommendation;
2. the rationale for that recommendation;
3. the meaningful tradeoff or consequence of accepting it;
4. a concise set of answer choices when choices are useful.

The orchestrator must record every user answer faithfully and relay it without reinterpretation, weakening, silent replacement, or merging it with the recommendation. If an answer is ambiguous in a way that materially changes the design, quote or closely paraphrase the ambiguity and ask one focused follow-up question within the batch.

Do not return to the designer for an update after each answer. After the complete planned batch, the orchestrator must return all recorded answers once so the designer performs one design update and one reassessment. Start another small batch whenever any unresolved blocking core question remains, whether previously known or newly exposed. Do not ask questions whose answers can no longer affect the design.

## Low-Impact Questions That Must Not Block Design

Low-impact questions must not block design progress or the DESIGN_READY gate. These include preferences whose alternatives preserve algorithm semantics, the primary mental model, the teaching arc, and the high-level beats, such as minor color, typography, spacing, timing, wording, or decorative choices unless accessibility or correctness makes them material.

Choose a reasonable default, record it under risks or best-effort notes when useful, and continue. The user may revise these details during the edit loop.

## DESIGN_READY Gate

DESIGN_READY passes only when all of the following are true:

- the design goal and audience are explicit;
- the algorithm variant and operational semantics are unambiguous;
- the primary mental model is explicit and technically faithful;
- likely viewer misconceptions and their preventions are identified;
- the sample input is suitable and its teaching rationale is stated;
- every applicable required design decision and teaching risk in the routed type-specific reference is addressed; when no matching type reference exists, the design instead records best-effort classification, the specific coverage risk, and the strengthened-review requirement;
- the core visual metaphor and visual semantics are defined;
- structure presentation, scene structure, and information hierarchy are defined;
- the teaching arc is coherent;
- the high-level animation beats expose the important state transitions and causal relationships;
- a recommended design and material alternatives include rationale and tradeoffs;
- all material user decisions are incorporated faithfully;
- zero unresolved blocking core questions remain;
- only low-impact items remain unresolved, and each is documented as a risk with its chosen best-effort default;
- the design document satisfies the required contract and self-check.

Once every DESIGN_READY condition passes, the process must stop asking design questions and stop adding design work. It must send the exact DESIGN_READY version of `animation_design.md` to an independent animation design review. The independent reviewer must write `animation_design_review.md`; any result other than `PASS` rolls the design back to DESIGN_DEVELOPMENT.

Only after `animation_design_review.md = PASS` may the process request explicit user approval of the exact reviewed version of `animation_design.md`. After that approval binds the same exact version, the design may proceed to faithful conversion into `pre_build_brief.md`; neither review nor approval alone authorizes conversion. Continuing to elaborate, clarify, request approval before review passes, convert before exact-version approval, or expand the design after the gate passes is a process failure.

## User Edit Loop

The user may edit `animation_design.md` directly. Every user edit creates a new version, invalidates the prior review result, and requires re-review before confirmation can be accepted. Edit impact determines whether the re-review is full or delta; no edit bypasses re-review.

After an edit, identify what changed, preserve the user's wording and intent, run the appropriate review scope, update the DESIGN_READY self-check, and present the reviewed document again for explicit confirmation. Silence, inactivity, or editing the file alone does not count as approval.

## Full Review Versus Delta Review

Use full review for the initial design, after changes to algorithm semantics, primary mental model, core visual metaphor or semantics, teaching arc, scene structure, high-level beats, or whenever change impact is uncertain. Full review checks the entire document and every DESIGN_READY condition.

Use delta review only for a clearly bounded edit whose effects can be traced completely. Delta review must inspect the changed text, all dependent sections, internal consistency, and the DESIGN_READY self-check. Escalate immediately to full review if the edit has cross-cutting effects or reveals an earlier inconsistency.

## Rollback Rules

If review finds a regression, contradiction, unsupported claim, lost user decision, or failed DESIGN_READY condition, roll the design state back to DESIGN_DEVELOPMENT. Do not silently restore old text over a user edit. Preserve the user's requested change in the decision record, explain the conflict, and resolve it through one focused core question only when the impact is material.

If downstream work reveals that the confirmed design is technically invalid or materially incomplete, stop downstream production and return to DESIGN_DEVELOPMENT. Re-review and explicit reconfirmation are required before downstream work resumes.

## Failure Conditions

The process fails if it:

- treats clarification as the primary deliverable instead of designing the teaching and presentation;
- asks a large questionnaire, asks multiple user-facing questions at once, or mixes unrelated decisions in one batch;
- omits the recommendation, rationale, or tradeoff from a core question;
- relays a user answer inaccurately or silently substitutes another choice;
- blocks on a low-impact preference;
- leaves the mental model, visual presentation, teaching arc, or high-level beats undesigned;
- declares DESIGN_READY while any gate condition is unmet or any unresolved blocking core question remains;
- continues questioning or elaborating after every DESIGN_READY condition passes;
- requests user approval before independent review records `PASS` in `animation_design_review.md`;
- accepts silence, inactivity, or an unreviewed edit as approval;
- uses delta review when the change requires full review;
- continues downstream work after the design has rolled back.
