# Quick Sort Animation Plan

## Goal

Teach Quick Sort on the input array `[50, 90, 70, 20, 10, 30, 40]`, sorting in ascending order.

The animation should make the partition idea visible: choose the rightmost value as the pivot, scan the current range, move values less than or equal to the pivot to the left side, then place the pivot in its final sorted position.

## Audience

Introductory algorithm learners who know arrays and comparisons, but may not yet understand how recursive partitioning produces a full sort.

## Algorithm Mode

- Primary mode: algorithm walkthrough
- Secondary focus: pointer and control-flow explainer

## Algorithm Variant

- Quick Sort with Lomuto partition
- Pivot: rightmost element of each active subarray
- Sort order: ascending

## Core State

- Array: `main`
- Active range: current recursive subarray
- Pivot pointer: rightmost element of the active range
- Scan pointer `j`: moves left to right through the range before the pivot
- Boundary pointer `i`: marks the end of the `<= pivot` region

## Visual Semantics

- Default element: neutral blue
- Active range: thin outlined band around the current subarray
- Current comparison: yellow
- Pivot: orange
- Sorted/fixed element: green
- Pointers: distinct labels above or below the array

## Invariants To Show

- During partition, values at or left of `i` are `<= pivot`.
- Values between `i + 1` and `j - 1` have been scanned and are `> pivot`.
- When the pivot is swapped into `i + 1`, that pivot position is final.
- Recursive calls only sort the ranges left and right of fixed pivots.

## Beats

1. Establish the input and the rightmost-pivot rule.
2. Start partitioning the full range with pivot `40`.
3. Scan `50`, `90`, and `70`; all are greater than `40`.
4. Move `20` to the left side because it is `<= 40`.
5. Move `10` and `30` to the left side.
6. Place pivot `40` into its final index.
7. Partition the left range `[20, 10, 30]` with pivot `30`.
8. Fix pivot `30`, then focus on `[20, 10]`.
9. Place `10` before `20`, completing the left side.
10. Partition the right range `[90, 70, 50]` with pivot `50`.
11. Place pivot `50`, leaving `[70, 90]`.
12. Fix pivot `90`, then mark `70` as the base case.
13. Show the final ascending array.

