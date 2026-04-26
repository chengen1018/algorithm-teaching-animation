from tracer import AlgorithmTracer

DATA = [1, 3, 5, 7, 9, 11, 13]
TARGET = 11


def binary_search_traced(data, target):
    tracer = AlgorithmTracer()
    arr = list(data)

    left = 0
    right = len(arr) - 1

    tracer.create_array("main", arr)
    tracer.create_pointer("p_left", "left", "main", left, position="bottom")
    tracer.create_pointer("p_right", "right", "main", right, position="bottom")

    while left <= right:
        mid = (left + right) // 2
        tracer.create_pointer("p_mid", "mid", "main", mid, position="top")
        tracer.highlight("main", [mid], "YELLOW")

        if arr[mid] == target:
            tracer.mark_sorted("main", [mid])
            tracer.unhighlight("main", [mid])
            tracer.remove_pointer("p_mid")
            break

        if arr[mid] < target:
            tracer.mark_excluded("main", list(range(left, mid + 1)))
            left = mid + 1
            tracer.move_pointer("p_left", "main", left)
        else:
            tracer.mark_excluded("main", list(range(mid, right + 1)))
            right = mid - 1
            tracer.move_pointer("p_right", "main", right)

        tracer.remove_pointer("p_mid")

    tracer.remove_pointer("p_left")
    tracer.remove_pointer("p_right")
    tracer.output()


if __name__ == "__main__":
    binary_search_traced(DATA, TARGET)
