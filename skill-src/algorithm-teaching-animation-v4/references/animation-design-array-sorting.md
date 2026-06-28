# Animation Design: Array Sorting

Use this reference for array-sorting animations after the common teaching design guidance has been applied. It adds decisions specific to how comparisons or updates, movement, identity, and progress are understood; it does not replace the process or artifact contracts.

## Required Design Decisions

### active comparison unit

The design must define the algorithm-appropriate active decision or update unit. For a comparison-based sort, state whether that unit is a pair, a key and candidate, a pivot and scanned item, or another exact set of elements; the comparison operands and result must become visible before the resulting change. For a non-comparison sort, identify the count, bucket placement, digit pass, distribution step, or other update that causes the next state change, and show its inputs and result without inventing a comparison.

### movement model

When elements move, the design must choose whether values swap, shift, copy, or move as persistent objects. Position must encode one stable meaning throughout the operation. Show enough of the path or intermediate vacancy to distinguish the chosen operation from a visually similar one. If the algorithm updates counts, buckets, or auxiliary storage instead, define that update model and do not imply element movement that does not occur.

### settled-progress expression

The design must define a progress model that matches the algorithm, such as a settled boundary, completed pass, processed digit, accumulated counts, filled buckets, or merged runs. It must not assume a contiguous growing settled region. If “settled” is meaningful, state exactly what it guarantees; otherwise use algorithm-appropriate progress language. Progress styling must remain distinct from the active decision or update and from untouched data, so viewers do not mistake attention for completion.

### temporary holding position

If an item leaves the array while others shift, the design must provide a visible temporary holding position and preserve the item's connection to the open slot. If the algorithm never holds an item outside the array, state that explicitly and do not invent a holding area that implies false state. Auxiliary counts or buckets must not be presented as a temporary holding position unless they actually contain array items.

### duplicate-value identity tracking

When relative order, movement, or bucket placement of equal values matters, the design must give those items persistent identities. Labels, tokens, or another non-color-only cue must let viewers distinguish value equality from object identity and observe stability or instability accurately. If identity is irrelevant to the stated goal, do not add tracking that implies stability is being evaluated.

## Teaching Risks

### movement that hides causality

Do not animate several swaps, shifts, placements, or auxiliary updates before showing the decision or update that caused them. For comparison-based sorts, separate comparison evidence from its result; for non-comparison sorts, retain the relevant count, digit, bucket, or distribution evidence until the cause-effect link is clear.

### settled styling that resembles active styling

When the design uses settled styling, do not make it resemble active styling. For algorithms without settled elements, distinguish the chosen progress model from the active update instead. Verify that a paused frame cannot make an in-progress item look complete or permanently placed.

### a sample that never demonstrates the defining operation

Do not choose a sample that avoids the algorithm's characteristic comparison, swap, shift, partition, merge, count update, bucket placement, digit pass, or other required operation. Identify that operation in advance and point to the exact sample moment that makes it necessary.
