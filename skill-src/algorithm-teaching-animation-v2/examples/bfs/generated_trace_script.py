from tracer import AlgorithmTracer


GRAPH = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F"],
    "D": [],
    "E": ["F"],
    "F": [],
}


def bfs_traced(graph, start):
    tracer = AlgorithmTracer()
    visited = set()
    queue = [start]

    tracer.create_graph(
        "g1",
        ["A", "B", "C", "D", "E", "F"],
        [["A", "B"], ["A", "C"], ["B", "D"], ["B", "E"], ["C", "F"]],
    )
    tracer.highlight_node("g1", start, "YELLOW")
    tracer.mark_visited("g1", start, "GREEN")
    visited.add(start)

    while queue:
        current = queue.pop(0)
        tracer.highlight_node("g1", current, "YELLOW")

        for neighbor in graph[current]:
            if neighbor not in visited:
                tracer.mark_frontier("g1", neighbor, "ORANGE")
                tracer.mark_visited("g1", neighbor, "GREEN")
                visited.add(neighbor)
                queue.append(neighbor)
                tracer.unhighlight_node("g1", neighbor)

        tracer.unhighlight_node("g1", current)

    tracer.output()


if __name__ == "__main__":
    bfs_traced(GRAPH, "A")
