# Specialized Design Reference Selection

## Purpose

Make the entry to `DESIGN_DEVELOPMENT` unambiguous: the main Agent must read the shared animation-design guide and then select at most one algorithm-specific reference when the algorithm matches a supported category.

## Scope

- Add a single selection table to `references/how-to-design-animation.md`.
- Update the `DESIGN_DEVELOPMENT` entry in `SKILL.md` to require following that table.
- Preserve the existing rule that algorithms outside the three supported categories use only the shared guide.

## Selection Contract

| Algorithm category | Required specialized reference |
| --- | --- |
| Array sorting | `references/animation-design-array-sorting.md` |
| Graph traversal | `references/animation-design-graph-traversal.md` |
| Search that repeatedly narrows a candidate interval or region | `references/animation-design-search.md` |
| Any other algorithm | None; use only `references/how-to-design-animation.md` |

The main Agent reads `confirmed_requirements.md`, the shared guide, and the one matching specialized reference before beginning design. It must not apply more than one specialized reference or invent specialized interval, traversal, or sorting semantics for an unmatched algorithm.

## Ownership

Selection happens only during `DESIGN_DEVELOPMENT`. Downstream stages consume the approved `animation_design.md`; they do not reselect or reread specialized design references.

## Validation

Repository text checks must verify that the shared guide contains all three reference paths and the no-match fallback, and that `SKILL.md` directs the main Agent to the shared guide's selection rules.
