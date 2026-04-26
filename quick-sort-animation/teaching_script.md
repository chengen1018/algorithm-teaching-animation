# Teaching Script

## Summary

- Algorithm: Quick Sort, Lomuto partition
- Input: `[50, 90, 70, 20, 10, 30, 40]`
- Output: `[10, 20, 30, 40, 50, 70, 90]`
- Trace source: `action_trace.json`

## Beats

### beat-001: Establish the input

- Visual focus: the full input array.
- Trace mapping: `beat_id: beat-001`
- Event: create the array and introduce Quick Sort.
- Teaching point: Quick Sort repeatedly fixes one pivot, then recursively sorts the two sides.
- Teaching note: The animation uses the rightmost value as the pivot for every active range.

### beat-002: Start the first partition

- Visual focus: active range `0..6`, pivot `40`, scan pointer `j`, boundary pointer `i`.
- Trace mapping: `beat_id: beat-002`
- Event: set the first active range and mark pivot `40`.
- Teaching point: `i` marks the end of the region known to be `<= pivot`; initially that region is empty.
- Teaching note: The pivot will not be moved until every other value in the range has been checked.

### beat-003: Scan values greater than the pivot

- Visual focus: `50`, `90`, and `70` as `j` moves.
- Trace mapping: `beat_id: beat-003`
- Event: compare three values against pivot `40` without moving the boundary.
- Teaching point: values greater than the pivot stay on the right side of the future pivot position.
- Teaching note: The empty `<= pivot` region is still empty after these three comparisons.

### beat-004: Move 20 to the left side

- Visual focus: value `20`, boundary pointer `i`, and the swap with the first position.
- Trace mapping: `beat_id: beat-004`
- Event: `20 <= 40`, so `i` advances and `20` is swapped into the left region.
- Teaching point: every successful comparison grows the `<= pivot` region by one slot.
- Teaching note: The swap is not cosmetic; it preserves the partition invariant.

### beat-005: Move 10 and 30 to the left side

- Visual focus: values `10` and `30` as they are each moved before the pivot.
- Trace mapping: `beat_id: beat-005`
- Event: both values are `<= 40`, so the boundary advances twice and both values are swapped left.
- Teaching point: the left side now contains all values seen so far that belong before `40`.
- Teaching note: The exact order inside the left side is not final yet; Quick Sort will sort it recursively.

### beat-006: Place pivot 40

- Visual focus: swap between pivot `40` and the first greater value after the boundary.
- Trace mapping: `beat_id: beat-006`
- Event: pivot `40` moves to index `3`.
- Teaching point: after partition, the pivot is fixed; all smaller values are left of it and all larger values are right of it.
- Teaching note: Quick Sort does not need to move `40` again.

### beat-007: Partition the left range

- Visual focus: active range `0..2`, pivot `30`, values `20` and `10`.
- Trace mapping: `beat_id: beat-007`
- Event: both `20` and `10` are `<= 30`.
- Teaching point: if every scanned value is already on the correct side, the boundary advances without a visible swap.
- Teaching note: Pivot `30` is already in the correct final position for this range.

### beat-008: Focus on range [20, 10]

- Visual focus: active range `0..1`, pivot `10`, comparison with `20`.
- Trace mapping: `beat_id: beat-008`
- Event: `20 > 10`, so the boundary does not move.
- Teaching point: the pivot must move in front of `20`.
- Teaching note: This small partition shows the same rule at a smaller scale.

### beat-009: Complete the left side

- Visual focus: swap `10` with `20`, then mark `10` and `20` as fixed.
- Trace mapping: `beat_id: beat-009`
- Event: pivot `10` moves to index `0`; the one-element range containing `20` is a base case.
- Teaching point: recursive base cases finish ranges of length one.
- Teaching note: The left half is now sorted as `[10, 20, 30]`.

### beat-010: Partition the right range

- Visual focus: active range `4..6`, pivot `50`, values `90` and `70`.
- Trace mapping: `beat_id: beat-010`
- Event: both scanned values are greater than `50`.
- Teaching point: the `<= pivot` region remains empty, so `50` must move to the front of this range.
- Teaching note: This mirrors the earlier `[20, 10]` case.

### beat-011: Place pivot 50

- Visual focus: swap pivot `50` with `90`.
- Trace mapping: `beat_id: beat-011`
- Event: pivot `50` moves to index `4`.
- Teaching point: the right side now only needs to sort `[70, 90]`.
- Teaching note: Fixed pivots divide the original problem into smaller independent ranges.

### beat-012: Finish [70, 90]

- Visual focus: active range `5..6`, pivot `90`, base case `70`.
- Trace mapping: `beat_id: beat-012`
- Event: `70 <= 90`, so pivot `90` is already fixed at the end; `70` is a one-element base case.
- Teaching point: when every remaining range has length zero or one, recursion is done.
- Teaching note: All elements now have fixed sorted positions.

### beat-013: Final sorted array

- Visual focus: entire array in sorted state.
- Trace mapping: `beat_id: beat-013`
- Event: show the final array.
- Teaching point: local partition decisions have accumulated into the global ascending order.
- Teaching note: The final order is `[10, 20, 30, 40, 50, 70, 90]`.

