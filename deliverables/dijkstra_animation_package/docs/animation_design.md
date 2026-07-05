# Animation Design: Dijkstra's Algorithm

## Canonical Example Graph and Stable Layout

The same undirected graph is used in all six Scenes. Node positions are fixed before any algorithm action and never move:

- `A`: far left, vertically centered.
- `B`: upper-left.
- `C`: lower-left.
- `D`: center.
- `E`: upper-center, directly above `D`.
- `F`: upper-right.

This placement forms a planar chain of triangles `A-B-C`, `B-C-D`, `B-D-E`, and `D-E-F`, so all nine edges can be drawn as straight segments without crossings. Weight labels sit beside the middle of their own edges on the open side of each triangle.

| Edge | Weight |
| --- | ---: |
| `A—B` | 4 |
| `A—C` | 2 |
| `B—C` | 1 |
| `B—D` | 5 |
| `B—E` | 7 |
| `C—D` | 8 |
| `D—E` | 2 |
| `D—F` | 6 |
| `E—F` | 3 |

When a current node has multiple neighbors, edges are checked in alphabetical node-label order as a deterministic teaching choice, not as a guarantee required by Dijkstra's algorithm.

## Scene 1: Problem and Goal
### Teaching Purpose
Establish the task of finding the shortest path from a specified start node to a specified target in a non-negatively weighted graph.

### Explanation Focus
The path with the fewest edges is not necessarily the path with the smallest total weight. The goal is to find the minimum-total-weight route from `A` to `F`.

### On-Screen Content
- The complete canonical undirected weighted graph with six nodes labeled `A` through `F`, all nine edges, and all weights visible from the start.
- Start badge on `A` and target badge on `F`.
- Short English labels: `Start`, `Target`, and `Find the minimum total weight`.
- Several visible routes from `A` to `F` with different accumulated weights.

### Concrete Animation Sequence
1. The six-node graph fades in with all non-negative edge weights visible.
2. Node `A` receives the `Start` badge, then node `F` receives the `Target` badge.
3. The three-edge route `A → B → D → F` is traced and accumulated as `4 + 5 + 6 = 15`.
4. The four-edge route `A → C → B → E → F` is traced and accumulated as `2 + 1 + 7 + 3 = 13`, establishing that fewer edges does not necessarily mean lower total weight.
5. Candidate-route emphasis clears while the graph remains fixed, and the prompt `Find the minimum total weight` becomes the sole focus.
6. All scene elements fade to blank before the next Scene.

## Scene 2: Core Concept
### Teaching Purpose
Build the central Dijkstra mental model: tentative distances are best-known values, and the smallest tentative distance among unfinalized nodes can be made final when all edge weights are non-negative.

### Explanation Focus
At each step, select the unfinalized node with the smallest tentative distance, finalize it, then use its outgoing edges to seek better routes to its neighbors. A finalized distance will not decrease later.

### On-Screen Content
- The same stable weighted graph introduced in Scene 1.
- A tentative-distance label beside each node: `0` at `A` and `∞` elsewhere at initialization.
- A compact legend distinguishing `Current`, `Tentative`, and `Finalized` states.
- A short rule line: `Choose the smallest unfinalized distance`.

### Concrete Animation Sequence
1. The graph fades in with `A = 0` and every other tentative-distance label set to `∞`.
2. All unfinalized distance labels briefly align visually for comparison; `A = 0` is identified as the minimum.
3. Node `A` changes from tentative to finalized when its minimum item is removed; a separate current outline marks it as the node whose edges are being processed.
4. Edges from current node `A` illuminate one at a time; each neighbor receives a finite tentative distance calculated from `0 + edge weight`.
5. The current outline clears after the neighbor checks. The finite tentative labels are compared, and the smallest one is elevated as the next node to finalize.
6. A non-negative-weight cue supports the conclusion that no later route through a farther unsettled node can reduce the selected minimum.
7. The selected node changes to finalized while all other tentative labels remain visible for comparison.
8. All scene elements fade to blank before the next Scene.

## Scene 3: Algorithm-Specific Data and State
### Teaching Purpose
Explain the Dijkstra-specific state needed to choose the next node, improve routes, and reconstruct the final path without teaching heap internals.

### Explanation Focus
Each node has a tentative distance and a predecessor. The min-priority queue orders discovered but unfinalized nodes by tentative distance. Removing the minimum finalizes that node's distance; a separate current outline remains while its neighboring edges are checked.

### On-Screen Content
- A stable weighted graph with distance labels beside nodes.
- A compact `Min-priority queue` strip containing `(node, distance)` items in ascending-distance order; its minimum-removal end is visibly marked.
- A compact predecessor row using entries such as `C ← B`.
- A persistent legend for `Undiscovered`, `Tentative`, and `Finalized`, plus a distinct `Current` outline that can overlay the finalized state.
- Short state rules: `distance[A] = 0`, `others = ∞`, and `previous = —`.

### Concrete Animation Sequence
1. The graph appears with `A = 0`, all other distances at `∞`, no predecessors, and queue item `(A, 0)` at the marked minimum end.
2. `(A, 0)` leaves the queue and moves visually toward node `A`; `A` changes from tentative to finalized and receives the current outline.
3. A neighbor of `A` is discovered: its distance changes from `∞` to a finite value, its predecessor changes from `—` to `A`, and its `(node, distance)` item enters the queue in sorted position.
4. A second neighbor is discovered through the same synchronized graph-to-state transition.
5. After all adjacent edges of `A` have been checked, its current outline clears while its finalized state remains.
6. The marked minimum end identifies which queue item will leave next; that item moves to its graph node, finalizes the node's distance, and applies the current outline.
7. A later distance improvement is previewed by changing one queue item's value and sliding it earlier in the ordered strip, while its predecessor entry updates at the same moment.
8. The state legend remains visible long enough to distinguish discovery, distance finalization, and the current neighbor-processing focus.
9. All scene elements fade to blank before the next Scene.

## Scene 4: One Key Action
### Teaching Purpose
Show one complete edge-relaxation decision slowly enough that the viewer can connect graph values to the distance, predecessor, and priority-queue updates.

### Explanation Focus
For current node `C` and neighbor `B`, compute the route through `C`, compare it with `B`'s existing tentative distance, and update all dependent state only because the new route is shorter.

### On-Screen Content
- A focused portion of the graph containing `A`, current/finalized node `C`, tentative node `B`, edge `C—B` of weight `1`, `dist[C] = 2`, and old `dist[B] = 4`.
- The comparison `dist[C] + w(C,B) < dist[B]?`, followed by `2 + 1 < 4`.
- Predecessor entry for `B`, initially `B ← A`.
- Min-priority queue containing `(B, 4)` and other candidates with larger values.

### Concrete Animation Sequence
1. The graph fragment, current outline on `C`, old distance `B = 4`, predecessor `B ← A`, and queue item `(B, 4)` appear together.
2. `dist[C] = 2` and edge weight `1` illuminate before copies of `2` and `1` move into the comparison formula.
3. The expression resolves from `dist[C] + w(C,B)` to `2 + 1 = 3`, then compares `3 < 4`.
4. The true result is emphasized; the route segment `C—B` brightens while the older predecessor edge `A—B` loses emphasis.
5. `dist[B]` changes from `4` to `3`.
6. The predecessor entry changes from `B ← A` to `B ← C`.
7. Queue item `(B, 4)` changes to `(B, 3)` and slides to its new sorted position.
8. A compact summary remains: `shorter → update distance, previous, queue`.
9. All scene elements fade to blank before the next Scene.

## Scene 5: Full Algorithm Demonstration
### Teaching Purpose
Apply the complete Dijkstra process from `A` until target `F` is finalized, showing every minimum extraction and every consequential relaxation on one stable example.

### Explanation Focus
The target is complete only when its minimum item is removed and its distance is finalized—not when it is first discovered. The priority queue, tentative distances, and predecessors remain synchronized with graph events.

### On-Screen Content
- The complete canonical graph in its fixed planar layout, with all nine edge weights visible.
- Start marker on `A`, target marker on `F`, node distance labels, the ordered min-priority queue, and predecessor entries.
- The same persistent state semantics: undiscovered, tentative, finalized, with a current outline over the node being processed.
- A small calculation area used only for the active relaxation.

### Concrete Animation Sequence
1. Initialize `A = 0`, all other distances to `∞`, all predecessors to `—`, and queue to `[(A,0)]`.
2. Remove `(A,0)`, finalize `A`, and apply the current outline. Relax `A—B` to set `B = 4`, `B ← A`; relax `A—C` to set `C = 2`, `C ← A`. The queue becomes `[(C,2),(B,4)]`, then the current outline clears.
3. Remove `(C,2)`, finalize/current-highlight `C`. The already-finalized edge to `A` is acknowledged without update. Relax `C—B`: `2 + 1 < 4`, so set `B = 3`, `B ← C`, and reorder its queue item. Discover `D = 10`, `D ← C`. The queue becomes `[(B,3),(D,10)]`.
4. Remove `(B,3)`, finalize/current-highlight `B`. Relax `B—D`: `3 + 5 < 10`, so set `D = 8`, `D ← B`. Discover `E = 10`, `E ← B`. The queue becomes `[(D,8),(E,10)]`.
5. Remove `(D,8)`, finalize/current-highlight `D`. Check `D—E`: `8 + 2 = 10`, which is not less than `E = 10`, so no state changes. Relax `D—F`: set `F = 14`, `F ← D`; the target is now tentative but explicitly not finished. The queue becomes `[(E,10),(F,14)]`.
6. Remove `(E,10)`, finalize/current-highlight `E`. Relax `E—F`: `10 + 3 < 14`, so set `F = 13`, change `F ← D` to `F ← E`, and update the queue to `[(F,13)]`.
7. Remove `(F,13)`. Node `F` changes from tentative to finalized; because it is the target, the stop condition activates without processing unrelated additional work.
8. The queue and calculation area recede while the final distance `13` and predecessor chain remain visible.
9. All scene elements fade to blank before the next Scene.

## Scene 6: Result and Recap
### Teaching Purpose
Reveal the final shortest route and connect it back to the three repeated Dijkstra actions that produced it.

### Explanation Focus
The finalized target distance is `13`. Following predecessor links backward reconstructs `A → C → B → E → F`. Dijkstra repeatedly removes the smallest tentative distance, finalizes it, and relaxes its edges; correctness here depends on non-negative edge weights.

### On-Screen Content
- The same graph and final distance/predecessor state from Scene 5.
- Final result label: `Shortest distance: 13`.
- Backward predecessor chain `F ← E ← B ← C ← A`, then the forward path `A → C → B → E → F`.
- Three short recap labels: `Extract minimum`, `Finalize distance`, `Relax edges`.
- A concise condition label: `Requires non-negative edge weights`.

### Concrete Animation Sequence
1. The final graph fades in with all finalized distances retained and `F = 13` emphasized.
2. Starting at `F`, predecessor edges illuminate backward in order: `F ← E`, `E ← B`, `B ← C`, `C ← A`.
3. The backward chain transforms into the forward route `A → C → B → E → F` while non-route edges dim.
4. Edge weights on the route illuminate in order and accumulate as `2 + 1 + 7 + 3 = 13`.
5. `Shortest distance: 13` appears beside the highlighted route.
6. The three recap labels appear one at a time—`Extract minimum`, `Finalize distance`, `Relax edges`—with brief matching emphasis on the queue, a finalized node, and a route edge.
7. `Requires non-negative edge weights` appears as the final condition beneath the recap.
8. The completed path and distance hold briefly, then every element fades to blank.
