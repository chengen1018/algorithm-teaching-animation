from tracer import AlgorithmTracer

DATA = [5, 1, 4, 2, 8]


def bubble_sort_traced(data):
    tracer = AlgorithmTracer()
    arr = list(data)
    n = len(arr)

    tracer.create_array("main", arr)
    tracer.create_pointer("p_j", "j", "main", 0, position="top")

    for i in range(n):
        for j in range(0, n - i - 1):
            tracer.move_pointer("p_j", "main", j)
            tracer.highlight("main", [j, j + 1], "YELLOW")

            if arr[j] > arr[j + 1]:
                tracer.swap("main", j, j + 1)
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

            tracer.unhighlight("main", [j, j + 1])

        tracer.mark_sorted("main", [n - i - 1])

    tracer.remove_pointer("p_j")
    tracer.output()


if __name__ == "__main__":
    bubble_sort_traced(DATA)
