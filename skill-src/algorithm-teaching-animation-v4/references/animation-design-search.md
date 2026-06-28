# Animation Design: Search

Use this reference only for interval or candidate-region narrowing searches whose teaching depends on eliminating part of a candidate region after each decision. It adds narrowing-search state and choreography decisions without redefining the common design workflow or document structure.

## Applicability

Apply the requirements below only when the algorithm maintains and narrows an explicit candidate interval or region. The interval convention, pointer, and excluded-region requirements must not be applied to linear, graph, substring, or other searches without candidate-region elimination. Those searches must use a matching specialized reference when one is available. When none is available, they must use the common teaching-design and process guidance, be marked best-effort, disclose the coverage risk, and receive strengthened review. They must not invent interval semantics.

## Required Design Decisions

### interval convention

The design must declare the exact interval convention, such as closed `[low, high]` or half-open `[low, high)`, and encode it consistently in labels, brackets, and region shading. Every endpoint update must preserve that convention visibly.

### pointer meaning

The design must define what each pointer names: a candidate endpoint, a probe position, an insertion boundary, or another precise role. Pointer labels and placement must prevent viewers from confusing an index with the value stored at that index.

### stopping rule

The design must state the success and failure stopping conditions in terms of the chosen interval convention. The final frame must show the state that satisfies the rule, not jump directly from the last comparison to a result caption.

### elimination logic

The design must show why a comparison proves that a region cannot contain the target. Highlight the compared values and relevant ordering fact before marking the eliminated region, so exclusion is evidence-based rather than magical disappearance.

### pointer choreography

The design must order each cycle as probe, comparison, conclusion, then pointer update. If multiple pointers change, sequence them or tie them to one shared conclusion so viewers can identify which comparison caused each move.

### excluded-region persistence

The design must keep excluded regions visible in a subdued but readable state until their role is understood. Persistence must communicate accumulated proof and shrinking possibility while leaving the active interval dominant.

## Teaching Risks

### deleting context too early

Do not remove excluded values immediately. Early deletion hides how the candidate set shrank and makes later pointer positions appear arbitrary; retain enough context to compare the old and new interval.

### visually implying the wrong interval convention

Do not place endpoint markers, brackets, or shading where they contradict the declared interval. Check boundary frames, especially the empty and one-element cases, because those frames expose off-by-one implications most clearly.

### moving pointers without showing the comparison that caused the move

Do not animate a pointer update as an unexplained navigation step. Keep the probe, target, comparison relation, and eliminated side visible through the move so viewers can reconstruct the decision.
