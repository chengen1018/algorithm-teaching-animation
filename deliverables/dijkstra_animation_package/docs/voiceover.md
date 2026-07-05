# Voiceover

## Summary

- **Language:** English (`en-US`)
- **Source script:** `teaching_script.md` with `script_review_result.md = PASS`
- **Structure:** One narration segment per approved teaching beat
- **Global pronunciation:** `Dijkstra` = "DYE-kstruh"
- **Sync rule:** Establish the listed scene hook before narration starts, and keep that visual focus stable until the segment ends.

## Scene 1 — Problem and Goal

### beat-1-1 — Introduce the weighted graph
- **Scene hook:** Full weighted graph visible; `A` marked `Start`; `F` marked `Target`.
- **Narration:** Our goal is to find a path from A to F with the smallest total edge weight.
- **Pacing target:** Clear opening; brief pause after naming the endpoints.

### beat-1-2 — Evaluate a route with fewer edges
- **Scene hook:** Route `A → B → D → F` begins tracing.
- **Narration:** This three-edge route has total weight four plus five plus six, which is fifteen.
- **Pacing target:** Match each spoken addend to its highlighted edge.

### beat-1-3 — Show why edge count is insufficient
- **Scene hook:** Route `A → C → B → E → F` begins tracing while the earlier total remains available.
- **Narration:** But this four-edge route totals thirteen. Fewer edges did not mean less weight, so we need a systematic way to find the minimum.
- **Pacing target:** Pause after "thirteen" before stating the contrast.

## Scene 2 — Core Concept

### beat-2-1 — Initialize tentative distances
- **Scene hook:** `A = 0`; every other node displays infinity; state legend visible.
- **Narration:** Each label is the best distance known so far. We begin with zero at A and infinity everywhere else.
- **Pacing target:** Even explanatory pace.

### beat-2-2 — Choose the smallest unfinalized distance
- **Scene hook:** Unfinalized distance labels align for comparison.
- **Narration:** Dijkstra always chooses the unfinalized node with the smallest tentative distance. Here, that node is A.
- **Pacing target:** Slight emphasis on "smallest tentative distance."

### beat-2-3 — Finalize and process the selected node
- **Scene hook:** `A` changes to finalized and receives the current outline.
- **Narration:** Removing the minimum finalizes A's distance. The separate current outline shows that we are now checking A's neighbors.
- **Pacing target:** Pause between finalization and current-state explanation.

### beat-2-4 — Discover `B` from `A`
- **Scene hook:** Edge `A—B` illuminates.
- **Narration:** From A, the edge of weight four gives B a tentative distance of four.
- **Pacing target:** Short, synchronized with the distance replacement.

### beat-2-5 — Discover `C` from `A`
- **Scene hook:** Edge `A—C` illuminates.
- **Narration:** The second edge gives C a tentative distance of two. That completes A's neighbor checks.
- **Pacing target:** Let the current outline clear after the second sentence.

### beat-2-6 — Select the next minimum
- **Scene hook:** `B = 4` and `C = 2` are compared.
- **Narration:** Two is smaller than four, so C is the next node selected.
- **Pacing target:** Brief comparison with emphasis on C.

### beat-2-7 — Finalize the safe minimum
- **Scene hook:** Non-negative-weight cue appears beside selected `C = 2`.
- **Narration:** Because every edge weight is non-negative, no later route through a farther node can reduce this minimum. C's distance can now be finalized.
- **Pacing target:** Deliberate reasoning; finalize C after the first sentence.

## Scene 3 — Algorithm-Specific Data and State

### beat-3-1 — Establish the synchronized state
- **Scene hook:** Graph distances, predecessor row, and min-priority queue are all visible.
- **Narration:** Distances hold the best known costs. Predecessors remember the route, and the min-priority queue orders discovered, unfinalized nodes by distance.
- **Pacing target:** One steady phrase per visible structure.

### beat-3-2 — Remove the queue minimum
- **Scene hook:** Queue item `(A, 0)` is ready at the marked minimum end.
- **Narration:** The minimum item leaves the queue and moves to A. That removal finalizes A and makes it the current node.
- **Pacing target:** Match the first sentence to queue motion and the second to state styling.

### beat-3-3 — Discover the first neighbor
- **Scene hook:** The first neighbor of `A` is ready to change from undiscovered to tentative.
- **Narration:** Discovering a neighbor updates three records together: its distance, its predecessor, and its position in the queue.
- **Pacing target:** Three-part cadence aligned to the synchronized updates.

### beat-3-4 — Discover the second neighbor
- **Scene hook:** The second neighbor of `A` is ready for the same synchronized transition.
- **Narration:** The second neighbor receives the same coordinated update. The ordered queue now reveals which candidate is smaller.
- **Pacing target:** Pause before referring to the ordered queue.

### beat-3-5 — Extract the next candidate
- **Scene hook:** The next item is exposed at the queue's minimum end.
- **Narration:** The smallest queued distance leaves next. Its node becomes finalized and current for the next neighbor checks.
- **Pacing target:** Match extraction, finalization, then current outline.

### beat-3-6 — Preview a later improvement
- **Scene hook:** One tentative queue item is ready to decrease and move earlier.
- **Narration:** A tentative value can still improve. When a shorter route appears, its distance, predecessor, and queue position all change before finalization.
- **Pacing target:** Emphasize the contrast between tentative and finalized.

## Scene 4 — One Key Action: Relaxation

### beat-4-1 — Establish the old candidate for `B`
- **Scene hook:** `C` is current at distance two; `B` is tentative at four through `A`; edge weight one is visible.
- **Narration:** B currently costs four through A. We now ask whether reaching B through C is shorter.
- **Pacing target:** Set up the question without beginning the calculation.

### beat-4-2 — Compute the route through `C`
- **Scene hook:** Values `2` and `1` are ready to enter the relaxation formula.
- **Narration:** Reaching C costs two, and the edge to B costs one more. The new candidate is three.
- **Pacing target:** Match two, one, and three to the formula animation.

### beat-4-3 — Compare new and old distances
- **Scene hook:** Candidate `3` and current value `4` are visible together.
- **Narration:** Three is less than four, so the route through C becomes the best known route to B.
- **Pacing target:** Pause slightly at the comparison result.

### beat-4-4 — Update the distance
- **Scene hook:** `B = 4` is ready to change.
- **Narration:** B's tentative distance changes from four to three.
- **Pacing target:** Short statement synchronized to the number change.

### beat-4-5 — Update the predecessor
- **Scene hook:** Predecessor entry `B ← A` is ready to change.
- **Narration:** The shorter route came from C, so B's predecessor changes from A to C.
- **Pacing target:** Synchronize the final phrase with the predecessor replacement.

### beat-4-6 — Update and reorder the queue
- **Scene hook:** Queue item `(B, 4)` is ready to decrease and slide.
- **Narration:** Finally, B's queue value becomes three and moves to its sorted position. A shorter route updates the distance, predecessor, and queue together.
- **Pacing target:** First sentence follows queue motion; second sentence summarizes after it settles.

## Scene 5 — Full Algorithm Demonstration

### beat-5-1 — Initialize the full run
- **Scene hook:** Full graph and support state show `A = 0`, all others infinity, no predecessors, and queue `[(A, 0)]`.
- **Narration:** For the full run, A starts at zero, every other distance starts at infinity, and A is the first queue item.
- **Pacing target:** Compact reset before iteration begins.

### beat-5-2 — Finalize `A`
- **Scene hook:** `(A, 0)` is ready to leave the queue.
- **Narration:** Removing the minimum finalizes A at distance zero and makes it current.
- **Pacing target:** Match extraction, finalization, and current outline.

### beat-5-3 — Discover `B` from `A`
- **Scene hook:** Edge `A—B` is active.
- **Narration:** The edge to B discovers distance four, with A as B's predecessor.
- **Pacing target:** Synchronize distance, predecessor, then queue insertion.

### beat-5-4 — Discover `C` from `A`
- **Scene hook:** Edge `A—C` is active.
- **Narration:** The edge to C discovers distance two, with A as predecessor. C moves ahead of B in the queue, completing A's checks.
- **Pacing target:** Pause before the queue-order consequence.

### beat-5-5 — Finalize `C`
- **Scene hook:** `(C, 2)` is at the queue minimum.
- **Narration:** C has the smallest tentative distance, so it is finalized next at two.
- **Pacing target:** Short extraction and finalization statement.

### beat-5-6 — Acknowledge finalized neighbor `A`
- **Scene hook:** Edge `C—A` illuminates while both endpoint states remain visible.
- **Narration:** The edge back to A needs no update because A is already finalized.
- **Pacing target:** Brief acknowledgement; keep all state unchanged.

### beat-5-7 — Improve `B` through `C`
- **Scene hook:** Calculation `2 + 1 < 4` is visible.
- **Narration:** Through C, B costs two plus one, which is less than four. B improves to three, with C as its predecessor.
- **Pacing target:** Match comparison, distance change, then predecessor change.

### beat-5-8 — Discover `D` through `C`
- **Scene hook:** Edge `C—D` is active.
- **Narration:** C also discovers D with tentative distance ten and predecessor C.
- **Pacing target:** Synchronize distance, predecessor, and queue insertion.

### beat-5-9 — Finalize `B`
- **Scene hook:** `(B, 3)` is at the queue minimum.
- **Narration:** B is now the smallest candidate, so its distance three becomes final.
- **Pacing target:** Short extraction and finalization statement.

### beat-5-10 — Improve `D` through `B`
- **Scene hook:** Calculation `3 + 5 < 10` is visible.
- **Narration:** Reaching D through B costs eight, which improves the old value ten. D's predecessor changes to B.
- **Pacing target:** Pause between the distance improvement and predecessor change.

### beat-5-11 — Discover `E` through `B`
- **Scene hook:** Edge `B—E` is active.
- **Narration:** B discovers E at distance ten with predecessor B. D remains first in the queue at eight.
- **Pacing target:** First sentence for the update; second for the resulting queue order.

### beat-5-12 — Finalize `D`
- **Scene hook:** `(D, 8)` is at the queue minimum.
- **Narration:** Eight is the smallest tentative value, so D is finalized and becomes current.
- **Pacing target:** Match extraction, finalization, and current outline.

### beat-5-13 — Reject an equal route to `E`
- **Scene hook:** Calculation `8 + 2 = 10` appears beside `E = 10`.
- **Narration:** Through D, the candidate for E is also ten. It is not smaller, so E's state does not change.
- **Pacing target:** Pause after the equality before the no-update result.

### beat-5-14 — Discover target `F`
- **Scene hook:** Edge `D—F` is active.
- **Narration:** D discovers the target F at distance fourteen. But F is only tentative, so the search is not finished.
- **Pacing target:** Emphasize "only tentative."

### beat-5-15 — Finalize `E`
- **Scene hook:** Queue shows `(E, 10)` before `(F, 14)`.
- **Narration:** E's distance ten is smaller than F's fourteen, so E must be finalized first.
- **Pacing target:** Clear comparison leading to extraction.

### beat-5-16 — Improve target `F` through `E`
- **Scene hook:** Calculation `10 + 3 < 14` is visible.
- **Narration:** Through E, F costs thirteen, which improves fourteen. F's predecessor changes from D to E.
- **Pacing target:** Match distance improvement, predecessor change, then queue update.

### beat-5-17 — Finalize the target and stop
- **Scene hook:** `(F, 13)` is the remaining queue minimum.
- **Narration:** F is now the minimum. Removing it finalizes thirteen, so the search can stop.
- **Pacing target:** Pause after identifying the minimum, then land firmly on the stop condition.

## Scene 6 — Result and Recap

### beat-6-1 — Start from the finalized result
- **Scene hook:** Final state appears with `F = 13` emphasized.
- **Narration:** The finalized shortest distance from A to F is thirteen.
- **Pacing target:** Brief result announcement.

### beat-6-2 — Follow predecessors backward
- **Scene hook:** Predecessor tracing begins at `F`.
- **Narration:** Following predecessors backward leads from F to E, then B, then C, and finally A.
- **Pacing target:** Match each spoken node to its illuminated predecessor edge.

### beat-6-3 — Present and verify the forward path
- **Scene hook:** Backward chain is ready to transform into the forward route.
- **Narration:** Reversing that chain gives A to C to B to E to F. Its weights are two plus one plus seven plus three, for a total of thirteen.
- **Pacing target:** Pause between naming the route and adding its weights.

### beat-6-4 — Recap the repeated actions
- **Scene hook:** Queue, finalized node, and route edge are available for matching emphasis.
- **Narration:** Dijkstra repeats three actions: extract the minimum, finalize its distance, and relax its edges.
- **Pacing target:** Three-part cadence matched to the recap labels.

### beat-6-5 — State the required condition
- **Scene hook:** Completed path and distance remain visible; non-negative condition label appears.
- **Narration:** This finalization rule requires every edge weight to be non-negative.
- **Pacing target:** Deliberate closing statement, then hold before fade-out.
