# Animation Design: Array Sorting

Use this reference for array-sorting animations after the common teaching design guidance has been applied. It adds decisions specific to how comparisons, movement, identity, and progress are understood; it does not replace the process or artifact contracts.

## Required Design Decisions

### active comparison unit

The design must define whether one active unit is a pair, a key and candidate, a pivot and scanned item, or another exact set of elements. The comparison operands and result must become visible before movement begins, so viewers can attribute the following change to the correct decision.

### movement model

The design must choose whether values swap, shift, copy, or move as persistent objects. Position must encode one stable meaning throughout the operation. Show enough of the path or intermediate vacancy to distinguish the chosen operation from a visually similar one.

### settled-progress expression

The design must state what “settled” guarantees and how the settled region grows. Its styling must remain visibly distinct from active comparison, temporary selection, and merely untouched data, so viewers do not mistake attention for correctness.

### temporary holding position

If an item leaves the array while others shift, the design must provide a visible temporary holding position and preserve the item's connection to the open slot. If the algorithm never holds an item outside the array, state that explicitly and do not invent a holding area that implies false state.

### duplicate-value identity tracking

The design must give equal-valued items persistent identities when their relative order or movement matters. Labels, tokens, or another non-color-only cue must let viewers distinguish value equality from object identity and observe stability or instability accurately.

## Teaching Risks

### movement that hides causality

Do not animate several swaps or shifts before showing the comparisons that caused them. Separate comparison evidence from its resulting movement, and retain the relevant operands until the cause-effect link is clear.

### settled styling that resembles active styling

Do not use nearly identical emphasis for settled and active elements. Define distinct encodings and verify that a paused frame cannot make an in-progress item look permanently placed.

### a sample that never demonstrates the defining operation

Do not choose a sample that avoids the algorithm's characteristic swap, shift, partition, merge, or other required operation. Identify that operation in advance and point to the exact sample moment that makes it necessary.
