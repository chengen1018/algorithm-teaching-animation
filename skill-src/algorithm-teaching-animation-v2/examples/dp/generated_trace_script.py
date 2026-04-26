from tracer import AlgorithmTracer

WEIGHTS = [1, 2]
VALUES = [1, 3]
CAPACITY = 2


def knapsack_traced(weights, values, capacity):
    tracer = AlgorithmTracer()
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    tracer.create_matrix("dp", n + 1, capacity + 1, dp)

    for i in range(1, n + 1):
        weight = weights[i - 1]
        value = values[i - 1]
        for w in range(1, capacity + 1):
            tracer.highlight_cell("dp", i, w, "YELLOW")
            tracer.highlight_cell("dp", i - 1, w, "ORANGE")
            best = dp[i - 1][w]
            used_dependency = False

            if weight <= w:
                tracer.highlight_cell("dp", i - 1, w - weight, "ORANGE")
                best = max(best, dp[i - 1][w - weight] + value)
                used_dependency = True

            dp[i][w] = best
            tracer.set_cell("dp", i, w, best)
            tracer.mark_cell("dp", i, w, "GREEN")
            tracer.unhighlight_cell("dp", i - 1, w)
            if used_dependency:
                tracer.unhighlight_cell("dp", i - 1, w - weight)

    tracer.output()


if __name__ == "__main__":
    knapsack_traced(WEIGHTS, VALUES, CAPACITY)
