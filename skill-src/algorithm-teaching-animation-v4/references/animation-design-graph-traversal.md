# Animation Design: Graph Traversal

Use this reference for graph traversal animations after applying the common teaching design guidance. It governs traversal-specific state and support structures without replacing the process or `animation_design.md` contract.

## Required Design Decisions

### queue or stack visibility

The design must show the queue or stack whenever its order determines future traversal behavior. Display the active end or ends, preserve item order, and synchronize each enqueue, dequeue, push, or pop with the graph event that caused it.

### visited timing

The design must define exactly when a node becomes visited, such as on discovery or on removal for processing. The visual state change must occur at that moment, because different timing changes whether duplicate frontier entries are possible.

### discovery versus processing

The design must assign distinct, persistent meanings to discovered and processed states. Show the transition between them and connect it to the support structure, so viewers do not infer that finding a node means all of its neighbors have already been handled.

### frontier or path emphasis

The design must choose whether the main teaching object is the frontier, the traversal tree, or a current path. Emphasis must support the algorithm and learning goal: breadth-first behavior needs frontier order, while depth-first reasoning may need stack or path continuity.

### BFS layer expansion

For BFS, the design must decide whether layer expansion is a teaching goal. When it is, the current layer and next layer must be visibly distinguished while layer membership remains separate from discovered and processed states; a node can be discovered into the next layer before it is processed. When layer expansion is not a teaching goal, do not add layer styling that competes with the queue or implies extra algorithmic state.

### sample topology and traversal setup

The design must make the graph's directedness, start node, and relevant topology explicit before traversal begins. The sample must expose only the structures needed by the teaching goal: branching for frontier growth, cycles or cross-edges for revisitation, duplicate-discovery pressure for visited timing, or neighbor-order effects for deterministic sequencing, as applicable. Do not require every sample to contain all of these structures.

### neighbor order

The design must state the neighbor visitation order and make that order observable before it affects the queue, stack, or path. If several orders are valid, identify the chosen one as a deterministic teaching choice rather than an algorithmic guarantee.

### stable graph layout

The design must fix node positions before traversal begins and keep them stable. Use highlights, edges, and support-structure updates to show state change; spatial movement must not imply that graph topology is changing.

## Teaching Risks

### conflating discovered and processed states

Do not reuse one visual state for both events when the distinction affects understanding. A viewer must be able to pause and tell whether a node is merely scheduled or has had its neighbors examined.

### moving graph nodes after introduction

Do not rearrange nodes to make later steps convenient. Movement forces viewers to rebuild the graph's spatial map and can falsely suggest changed adjacency; solve crowding before traversal starts.

### hiding a teaching-critical support structure

Do not omit the queue, stack, or equivalent frontier representation when it explains traversal order. If space requires simplification, reduce decorative graph detail before hiding the structure that causes the next node choice.
