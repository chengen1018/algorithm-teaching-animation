# Teaching Script

## Summary

- **Algorithm:** Dijkstra's algorithm.
- **Teaching goal:** Help viewers understand Dijkstra's central idea and follow how it solves a shortest-path problem on a non-negatively weighted graph.
- **Problem:** Find the minimum-total-weight route from start node `A` to target node `F`.
- **Key semantics:** Tentative distances are the best values known so far. Repeatedly remove the smallest tentative distance from the min-priority queue, finalize that node, and relax its neighboring edges. A discovered target is not complete until its minimum item is removed and its distance is finalized. The reasoning depends on non-negative edge weights.
- **Language:** English voiceover and English on-screen text.
- **Stable example:** Use the same fixed undirected graph in all six Scenes, with edges `A—B:4`, `A—C:2`, `B—C:1`, `B—D:5`, `B—E:7`, `C—D:8`, `D—E:2`, `D—F:6`, and `E—F:3`.

## Scene 1 — Problem and Goal

### Beat 1.1 — Introduce the weighted graph

- **Viewer goal:** Recognize the graph, its edge weights, and the start-to-target task.
- **Algorithm moment:** Before the algorithm begins.
- **Visual focus:** The complete six-node graph with all nine non-negative weights, then the `Start` badge at `A` and the `Target` badge at `F`.
- **Teaching note:** The problem is defined by total path weight, not simply by graph connectivity.
- **Progress cue:** The fixed graph, start, and target are established for the rest of the lesson.
- **Voiceover intent:** State that the goal is to find a path from `A` to `F` with the smallest total edge weight.

### Beat 1.2 — Evaluate a route with fewer edges

- **Viewer goal:** See how a route's total weight is calculated.
- **Algorithm moment:** Compare candidate routes before introducing Dijkstra's procedure.
- **Visual focus:** Trace `A → B → D → F` and accumulate `4 + 5 + 6 = 15`.
- **Teaching note:** A path must be judged by the sum of its weights.
- **Progress cue:** One candidate route has a known total of `15`.
- **Voiceover intent:** Explain that this three-edge route costs fifteen.

### Beat 1.3 — Show why edge count is insufficient

- **Viewer goal:** Understand that fewer edges need not mean lower total weight.
- **Algorithm moment:** Motivate the need for a weighted shortest-path algorithm.
- **Visual focus:** Trace `A → C → B → E → F` and accumulate `2 + 1 + 7 + 3 = 13`, with the earlier total `15` available for comparison.
- **Teaching note:** The four-edge route is lighter than the three-edge route, so visual or edge-count intuition is unreliable.
- **Progress cue:** The prompt `Find the minimum total weight` remains after route emphasis clears.
- **Voiceover intent:** Contrast thirteen with fifteen and frame Dijkstra's algorithm as a systematic way to find the true minimum.

## Scene 2 — Core Concept

### Beat 2.1 — Initialize tentative distances

- **Viewer goal:** Interpret tentative distances as the best known costs from `A`.
- **Algorithm moment:** Initialization.
- **Visual focus:** Distance `0` beside `A`, `∞` beside every other node, and the `Current`, `Tentative`, and `Finalized` legend.
- **Teaching note:** Only the start is reachable with a known cost at initialization.
- **Progress cue:** `A = 0`; all other nodes remain unfinalized at `∞`.
- **Voiceover intent:** Explain that each label records the best distance known so far, beginning with zero at the start and infinity elsewhere.

### Beat 2.2 — Choose the smallest unfinalized distance

- **Viewer goal:** Understand Dijkstra's greedy selection rule.
- **Algorithm moment:** Select the first node for finalization.
- **Visual focus:** Align or compare the unfinalized distance labels and identify `A = 0` under `Choose the smallest unfinalized distance`.
- **Teaching note:** The next algorithm action is determined by the smallest tentative value.
- **Progress cue:** `A` is selected as the minimum candidate.
- **Voiceover intent:** State that Dijkstra always chooses the unfinalized node with the smallest tentative distance.

### Beat 2.3 — Finalize and process the selected node

- **Viewer goal:** Distinguish finalization from the temporary current-processing focus.
- **Algorithm moment:** Remove the selected minimum and begin checking its edges.
- **Visual focus:** `A` changes to finalized and receives the separate current outline.
- **Teaching note:** Finalized is a persistent distance state; current identifies whose outgoing edges are being processed now.
- **Progress cue:** `A` is finalized and current; all other nodes remain unfinalized.
- **Voiceover intent:** Explain that removing the minimum finalizes its distance, while the current outline marks the active neighbor checks.

### Beat 2.4 — Discover `B` from `A`

- **Viewer goal:** See how processing the current node produces a finite tentative distance for one neighbor.
- **Algorithm moment:** Check edge `A—B`.
- **Visual focus:** Illuminate `A—B` and replace `B = ∞` with the candidate computed from `0 + 4`.
- **Teaching note:** A neighbor check turns the previously unknown route to `B` into a tentative candidate.
- **Progress cue:** `B` now has a finite tentative distance while `A` remains finalized and current.
- **Voiceover intent:** Explain that the edge from `A` offers a tentative distance of four to `B`.

### Beat 2.5 — Discover `C` from `A`

- **Viewer goal:** Apply the same neighbor-update rule to the other neighbor of `A`.
- **Algorithm moment:** Check edge `A—C`.
- **Visual focus:** Illuminate `A—C`, replace `C = ∞` with the candidate computed from `0 + 2`, then clear `A`'s current outline.
- **Teaching note:** Each outgoing edge is checked independently, and current processing ends after the last neighbor check.
- **Progress cue:** `A` remains finalized without the current outline; `B = 4` and `C = 2` remain tentative.
- **Voiceover intent:** Explain that the second edge gives `C` a tentative distance of two, completing `A`'s neighbor checks.

### Beat 2.6 — Select the next minimum

- **Viewer goal:** Apply Dijkstra's greedy rule to the finite tentative values.
- **Algorithm moment:** Compare `B = 4` and `C = 2` and select the next node.
- **Visual focus:** Align or compare the remaining tentative labels and elevate `C = 2` as the smallest.
- **Teaching note:** The smallest unfinalized tentative value determines the next candidate for finalization.
- **Progress cue:** `C` is selected as the next minimum but has not yet changed state.
- **Voiceover intent:** State that two is smaller than four, so `C` is the next node selected.

### Beat 2.7 — Finalize the safe minimum

- **Viewer goal:** Connect non-negative edge weights to the safety of finalizing the selected minimum.
- **Algorithm moment:** Justify and finalize `C = 2`.
- **Visual focus:** A non-negative-weight cue supports `C = 2`, then `C` changes from tentative to finalized.
- **Teaching note:** A later route through a farther unfinalized node cannot return with a smaller total when every added edge is non-negative.
- **Progress cue:** `C = 2` is finalized; `B = 4` remains tentative and available for future improvement.
- **Voiceover intent:** Explain that non-negative weights prevent a later route from reducing this selected minimum, so `C`'s distance can be finalized.

## Scene 3 — Algorithm-Specific Data and State

### Beat 3.1 — Establish the synchronized state

- **Viewer goal:** Identify the three records Dijkstra uses: distance, predecessor, and ordered candidates.
- **Algorithm moment:** Full data-state initialization.
- **Visual focus:** `A = 0`, all other distances `∞`, predecessor entries `—`, and queue `[(A,0)]` at the marked minimum end.
- **Teaching note:** Distances guide selection, predecessors retain route information, and the min-priority queue orders discovered but unfinalized nodes.
- **Progress cue:** The graph and all support structures show one consistent initial state.
- **Voiceover intent:** Introduce what each visible structure contributes without explaining heap internals.

### Beat 3.2 — Remove the queue minimum

- **Viewer goal:** Connect minimum extraction to graph-state finalization.
- **Algorithm moment:** Remove `(A,0)`.
- **Visual focus:** `(A,0)` leaves the marked queue end, moves toward `A`, and `A` becomes finalized with a current outline.
- **Teaching note:** Queue removal is the event that finalizes the node's distance.
- **Progress cue:** `A` is no longer in the queue and is now the current finalized node.
- **Voiceover intent:** Explain that the minimum queue item determines the next node to finalize and process.

### Beat 3.3 — Discover the first neighbor

- **Viewer goal:** Follow one discovery across all synchronized structures.
- **Algorithm moment:** Process the first neighbor of `A` in alphabetical order.
- **Visual focus:** The neighbor changes from `∞` to a finite distance, its predecessor changes from `—` to `A`, and its queue item enters in sorted position.
- **Teaching note:** A single successful discovery updates distance, predecessor, and queue together.
- **Progress cue:** One discovered neighbor is tentative and represented consistently in every state view.
- **Voiceover intent:** Describe how a newly known route creates both a tentative distance and the information needed to trace it back.

### Beat 3.4 — Discover the second neighbor

- **Viewer goal:** Reinforce that each neighbor check applies the same synchronized transition.
- **Algorithm moment:** Process the second neighbor of `A`.
- **Visual focus:** The second finite distance, predecessor `A`, and newly inserted queue item, with queue items sorted by distance.
- **Teaching note:** The queue now exposes which discovered, unfinalized node has the smallest tentative distance.
- **Progress cue:** Both neighbors of `A` are tentative candidates; `A`'s current outline clears while finalization remains.
- **Voiceover intent:** Emphasize that the ordered queue is now ready to select the smaller candidate.

### Beat 3.5 — Extract the next candidate

- **Viewer goal:** See the state cycle repeat from queue to graph.
- **Algorithm moment:** Remove the next item at the marked minimum end.
- **Visual focus:** The minimum queue item moves to its node, which becomes finalized and receives the current outline.
- **Teaching note:** Selection is always based on the currently smallest tentative distance.
- **Progress cue:** A new finalized/current node is ready to check its neighbors.
- **Voiceover intent:** Reiterate the queue-to-finalization connection in the next iteration.

### Beat 3.6 — Preview a later improvement

- **Viewer goal:** Understand that a tentative value and its predecessor can still improve before finalization.
- **Algorithm moment:** A successful later relaxation.
- **Visual focus:** One queue item's distance decreases and slides earlier in the ordered strip while its predecessor entry changes at the same moment.
- **Teaching note:** Tentative means best known so far, not permanent; finalized is the state that no longer decreases.
- **Progress cue:** The improved candidate occupies its new correct queue position, and the state legend remains visible for comparison.
- **Voiceover intent:** Explain that finding a shorter route updates all dependent tentative state before the node is finalized.

## Scene 4 — One Key Action: Relaxation

### Beat 4.1 — Establish the old candidate for `B`

- **Viewer goal:** Read the complete local state before a relaxation decision.
- **Algorithm moment:** Current node `C` is about to check neighbor `B`.
- **Visual focus:** `dist[C] = 2`, edge `C—B` with weight `1`, old `dist[B] = 4`, predecessor `B ← A`, and queue item `(B,4)`.
- **Teaching note:** The decision must compare a newly computed route against the existing best-known route.
- **Progress cue:** `B` still has the old tentative route through `A` with cost `4`.
- **Voiceover intent:** Set up the question: is reaching `B` through `C` shorter than the current value four?

### Beat 4.2 — Compute the route through `C`

- **Viewer goal:** Map values on the graph into the relaxation formula.
- **Algorithm moment:** Evaluate `dist[C] + w(C,B)`.
- **Visual focus:** Copies of `2` and `1` move into `dist[C] + w(C,B)` and resolve to `2 + 1 = 3`.
- **Teaching note:** Relaxation tests a complete candidate distance, not the edge weight by itself.
- **Progress cue:** The new candidate for `B` is `3`; no state has changed yet.
- **Voiceover intent:** Explain that the route through `C` costs two to reach `C`, plus one more to reach `B`.

### Beat 4.3 — Compare new and old distances

- **Viewer goal:** Understand the condition that authorizes an update.
- **Algorithm moment:** Test `3 < 4`.
- **Visual focus:** The true comparison and the brightened `C—B` route segment while the older predecessor edge `A—B` loses emphasis.
- **Teaching note:** State changes occur only because the new candidate is strictly shorter.
- **Progress cue:** The new route through `C` has won the comparison.
- **Voiceover intent:** State that three is less than four, so the route through `C` becomes the best known route to `B`.

### Beat 4.4 — Update the distance

- **Viewer goal:** Associate a successful relaxation with the new tentative value.
- **Algorithm moment:** Replace `dist[B]`.
- **Visual focus:** `B = 4` changes to `B = 3`.
- **Teaching note:** The node label must reflect the newly proven best-known cost.
- **Progress cue:** `B`'s tentative distance is now `3`.
- **Voiceover intent:** Say that `B`'s tentative distance changes from four to three.

### Beat 4.5 — Update the predecessor

- **Viewer goal:** See how route reconstruction information follows the improved distance.
- **Algorithm moment:** Replace `B`'s predecessor.
- **Visual focus:** `B ← A` changes to `B ← C`.
- **Teaching note:** The predecessor records which previous node produced the current best-known value.
- **Progress cue:** The best-known route to `B` now points back through `C`.
- **Voiceover intent:** Explain that `B`'s predecessor must also change because the shorter candidate came from `C`.

### Beat 4.6 — Update and reorder the queue

- **Viewer goal:** See the final dependent state change caused by relaxation.
- **Algorithm moment:** Decrease the queue value for `B`.
- **Visual focus:** `(B,4)` changes to `(B,3)` and slides to its sorted position, followed by `shorter → update distance, previous, queue`.
- **Teaching note:** Queue order must match the improved tentative distances used by the next greedy selection.
- **Progress cue:** Distance, predecessor, and queue agree on the improved route.
- **Voiceover intent:** Summarize that a shorter route updates the distance, predecessor, and priority queue together.

## Scene 5 — Full Algorithm Demonstration

### Beat 5.1 — Initialize the full run

- **Viewer goal:** Recognize the complete initial state before iteration begins.
- **Algorithm moment:** Set `A = 0`, all other distances `∞`, all predecessors `—`, and queue `[(A,0)]`.
- **Visual focus:** The complete stable graph, node labels, predecessor entries, and ordered queue.
- **Teaching note:** This run applies the same rules already introduced, now without skipping consequential updates.
- **Progress cue:** Only `A` is in the queue; no node has yet been finalized.
- **Voiceover intent:** Briefly restate the initial distances and the first minimum candidate.

### Beat 5.2 — Finalize `A`

- **Viewer goal:** Start the repeated extract-finalize-relax cycle.
- **Algorithm moment:** Remove `(A,0)` and mark `A` finalized/current.
- **Visual focus:** The queue minimum moving to `A` and the current outline appearing.
- **Teaching note:** `A`'s distance zero is now final.
- **Progress cue:** `A` is current and ready to check neighbors alphabetically.
- **Voiceover intent:** State that the minimum item finalizes `A` at distance zero.

### Beat 5.3 — Discover `B` from `A`

- **Viewer goal:** Follow the first source-neighbor discovery across distance, predecessor, and queue state.
- **Algorithm moment:** Relax `A—B`.
- **Visual focus:** Set `B = 4`, set `B ← A`, and insert `(B,4)` into the queue.
- **Teaching note:** The direct edge from the source establishes the first tentative route to `B`.
- **Progress cue:** `B` is tentative at `4`; `A` remains finalized and current for its next neighbor check.
- **Voiceover intent:** Explain that the direct edge from `A` discovers `B` with distance four and predecessor `A`.

### Beat 5.4 — Discover `C` from `A`

- **Viewer goal:** Follow the second source-neighbor discovery and the resulting queue order.
- **Algorithm moment:** Relax `A—C`.
- **Visual focus:** Set `C = 2`, set `C ← A`, insert `(C,2)` ahead of `(B,4)`, show queue `[(C,2),(B,4)]`, then clear `A`'s current outline.
- **Teaching note:** After all of `A`'s neighbors are checked, the ordered queue exposes `C` as the next minimum.
- **Progress cue:** `A` remains finalized; `C` is the queue minimum at `2`.
- **Voiceover intent:** Explain that `A` also discovers `C` at two, which places `C` first in the queue and completes `A`'s checks.

### Beat 5.5 — Finalize `C`

- **Viewer goal:** Follow the queue's next greedy choice.
- **Algorithm moment:** Remove `(C,2)` and mark `C` finalized/current.
- **Visual focus:** `(C,2)` leaves the queue and `C` receives finalized/current styling.
- **Teaching note:** The smallest remaining tentative distance, two, becomes final.
- **Progress cue:** `C` is finalized and current, ready to check its neighbors in alphabetical order.
- **Voiceover intent:** Explain that `C` is finalized next because its tentative distance two is the queue minimum.

### Beat 5.6 — Acknowledge finalized neighbor `A`

- **Viewer goal:** Understand why an edge to an already-finalized neighbor causes no update.
- **Algorithm moment:** Check `C—A` before the other neighbors of `C`.
- **Visual focus:** Briefly illuminate `C—A` and the finalized state at `A`, with all distance, predecessor, and queue entries unchanged.
- **Teaching note:** The neighbor is already finalized, so this check produces no state transition.
- **Progress cue:** `C` remains current; `A` remains finalized; the algorithm proceeds to `C—B`.
- **Voiceover intent:** State that the edge back to finalized `A` needs no update.

### Beat 5.7 — Improve `B` through `C`

- **Viewer goal:** Apply the previously taught relaxation to the full run.
- **Algorithm moment:** Check `C—B` and resolve `2 + 1 < 4`.
- **Visual focus:** Change `B = 4` to `3`, `B ← A` to `B ← C`, and reorder its queue item.
- **Teaching note:** An unfinalized distance can improve when a shorter route is discovered.
- **Progress cue:** `B` is now the smallest tentative candidate at distance `3`.
- **Voiceover intent:** State that going through `C` improves the route to `B` from four to three.

### Beat 5.8 — Discover `D` through `C`

- **Viewer goal:** Follow the remaining consequential update from current node `C`.
- **Algorithm moment:** Relax `C—D`.
- **Visual focus:** Set `D = 10`, `D ← C`, and end with queue `[(B,3),(D,10)]`; then clear `C`'s current outline.
- **Teaching note:** The new candidate to `D` is tentative and may still improve.
- **Progress cue:** `C` remains finalized; `B` is the queue minimum.
- **Voiceover intent:** Explain that `C` first discovers `D` with a tentative distance of ten.

### Beat 5.9 — Finalize `B`

- **Viewer goal:** Continue the greedy selection cycle.
- **Algorithm moment:** Remove `(B,3)` and mark `B` finalized/current.
- **Visual focus:** Queue extraction and the state change at `B`.
- **Teaching note:** `B`'s improved value three is now final.
- **Progress cue:** `B` is current and its consequential neighbor relaxations follow.
- **Voiceover intent:** State that `B`, now the smallest candidate, is finalized at three.

### Beat 5.10 — Improve `D` through `B`

- **Viewer goal:** See a tentative distance improve again before finalization.
- **Algorithm moment:** Check `B—D` and resolve `3 + 5 < 10`.
- **Visual focus:** Change `D = 10` to `8`, `D ← C` to `D ← B`, and update its queue item.
- **Teaching note:** The queue and predecessor must track the newly shorter route.
- **Progress cue:** `D`'s best-known distance is `8` through `B`.
- **Voiceover intent:** Explain that the route through `B` reduces `D` from ten to eight.

### Beat 5.11 — Discover `E` through `B`

- **Viewer goal:** Establish the next target-side candidate.
- **Algorithm moment:** Relax `B—E`.
- **Visual focus:** Set `E = 10`, `E ← B`; end with queue `[(D,8),(E,10)]` and clear `B`'s current outline.
- **Teaching note:** `D` and `E` are both tentative, ordered by their current best distances.
- **Progress cue:** `D` is the queue minimum at `8`.
- **Voiceover intent:** State that `B` discovers `E` at distance ten, while `D` remains next.

### Beat 5.12 — Finalize `D`

- **Viewer goal:** Track the next extraction and finalization.
- **Algorithm moment:** Remove `(D,8)` and mark `D` finalized/current.
- **Visual focus:** The queue item moves to `D`; `D` receives finalized/current styling.
- **Teaching note:** `D`'s shortest distance is fixed at eight.
- **Progress cue:** `D` begins its consequential checks toward `E` and `F`.
- **Voiceover intent:** State that `D` is finalized because eight is the smallest tentative value.

### Beat 5.13 — Reject an equal route to `E`

- **Viewer goal:** Understand that relaxation requires a strictly shorter candidate.
- **Algorithm moment:** Check `D—E`: `8 + 2 = 10`, not less than `E = 10`.
- **Visual focus:** The equality comparison in the small calculation area and the unchanged state for `E`.
- **Teaching note:** An equal candidate does not satisfy the approved strict-less-than update condition.
- **Progress cue:** `E` remains `10` with predecessor `B`.
- **Voiceover intent:** Explain that the route through `D` ties the current value, so nothing changes.

### Beat 5.14 — Discover target `F`

- **Viewer goal:** Distinguish discovering the target from completing the algorithm.
- **Algorithm moment:** Relax `D—F`.
- **Visual focus:** Set `F = 14`, `F ← D`, mark `F` tentative, and show queue `[(E,10),(F,14)]`; then clear `D`'s current outline.
- **Teaching note:** A target with a tentative distance can still receive a better route later.
- **Progress cue:** `F` is discovered but explicitly not finished; `E` is still the smaller queue item.
- **Voiceover intent:** Stress that finding `F` at fourteen does not finish the search because `F` has not been removed as the minimum.

### Beat 5.15 — Finalize `E`

- **Viewer goal:** See why work continues after target discovery.
- **Algorithm moment:** Remove `(E,10)` and mark `E` finalized/current.
- **Visual focus:** `(E,10)` leaves the queue while tentative `(F,14)` remains.
- **Teaching note:** Dijkstra must process the smaller candidate `E` before it can finalize `F`.
- **Progress cue:** `E` is current; `F` remains tentative at `14`.
- **Voiceover intent:** Explain that distance ten is smaller than fourteen, so `E` must be finalized first.

### Beat 5.16 — Improve target `F` through `E`

- **Viewer goal:** See the target's tentative route improve before finalization.
- **Algorithm moment:** Check `E—F` and resolve `10 + 3 < 14`.
- **Visual focus:** Change `F = 14` to `13`, `F ← D` to `F ← E`, and queue to `[(F,13)]`; then clear `E`'s current outline.
- **Teaching note:** This update proves why first discovery was not a safe stopping point.
- **Progress cue:** `F` is the sole queue candidate at tentative distance `13`.
- **Voiceover intent:** Explain that the route through `E` improves the target from fourteen to thirteen.

### Beat 5.17 — Finalize the target and stop

- **Viewer goal:** Identify the correct target stopping condition.
- **Algorithm moment:** Remove `(F,13)` and activate the stop condition.
- **Visual focus:** `F` changes from tentative to finalized; the queue and calculation area recede while distance `13` and predecessor links remain.
- **Teaching note:** The answer becomes complete when the target's minimum item is removed and its distance is finalized.
- **Progress cue:** The finalized target distance is `13`, ready for path reconstruction.
- **Voiceover intent:** State that `F` is now the minimum, so thirteen is final and the search can stop.

## Scene 6 — Result and Recap

### Beat 6.1 — Start from the finalized result

- **Viewer goal:** Recognize the final shortest distance before reconstructing the route.
- **Algorithm moment:** Post-processing after target finalization.
- **Visual focus:** The final graph and state with `F = 13` emphasized.
- **Teaching note:** Finalized distance and predecessor state contain both the cost and the route.
- **Progress cue:** `Shortest distance: 13` is supported by the final algorithm state.
- **Voiceover intent:** Announce that the finalized shortest distance from `A` to `F` is thirteen.

### Beat 6.2 — Follow predecessors backward

- **Viewer goal:** Understand how the stored predecessors reconstruct the solution.
- **Algorithm moment:** Trace `F ← E ← B ← C ← A`.
- **Visual focus:** Illuminate predecessor edges backward, one at a time, beginning at `F`.
- **Teaching note:** Each predecessor identifies the previous node on the best route that produced the final value.
- **Progress cue:** The complete backward chain reaches the start node `A`.
- **Voiceover intent:** Explain that following predecessors from the target leads backward through `E`, `B`, and `C` to `A`.

### Beat 6.3 — Present and verify the forward path

- **Viewer goal:** Read the final route in travel order and verify its total.
- **Algorithm moment:** Transform the backward chain into `A → C → B → E → F`.
- **Visual focus:** Dim non-route edges, highlight the forward path, and accumulate `2 + 1 + 7 + 3 = 13` beside `Shortest distance: 13`.
- **Teaching note:** The reconstructed route and finalized distance agree numerically.
- **Progress cue:** The shortest route and its total weight are both explicit.
- **Voiceover intent:** Name the final route and add its edge weights to confirm the total of thirteen.

### Beat 6.4 — Recap the repeated actions

- **Viewer goal:** Retain the operational core of Dijkstra's algorithm.
- **Algorithm moment:** Summarize the full run.
- **Visual focus:** Show `Extract minimum`, `Finalize distance`, and `Relax edges` one at a time, with matching emphasis on the queue, a finalized node, and a route edge.
- **Teaching note:** These three actions form the repeated structure that produced the answer.
- **Progress cue:** The viewer has a concise procedure that maps back to the completed example.
- **Voiceover intent:** Recap that Dijkstra repeatedly extracts the minimum, finalizes its distance, and relaxes its edges.

### Beat 6.5 — State the required condition

- **Viewer goal:** Remember when the finalization reasoning applies.
- **Algorithm moment:** Final correctness condition.
- **Visual focus:** `Requires non-negative edge weights` beneath the recap while the completed route and distance remain visible.
- **Teaching note:** The lesson's finalization argument depends on every edge weight being non-negative.
- **Progress cue:** Hold the path, distance, repeated actions, and required condition together before fading to blank.
- **Voiceover intent:** Close by stating that Dijkstra's algorithm requires non-negative edge weights.
