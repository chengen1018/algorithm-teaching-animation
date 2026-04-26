from tracer import AlgorithmTracer


DATA = [50, 90, 70, 20, 10, 30, 40]


def compare_and_maybe_move(tracer, arr, i, j, high, beat_id):
    pivot = arr[high]
    tracer.move_pointer("p_j", "main", j, beat_id)
    tracer.highlight("main", [j], "YELLOW", beat_id)

    if arr[j] <= pivot:
        i += 1
        tracer.move_pointer("p_i", "main", i, beat_id)
        if i != j:
            tracer.swap("main", i, j, beat_id)
            arr[i], arr[j] = arr[j], arr[i]

    tracer.unhighlight("main", [j], beat_id)
    return i


def start_partition(tracer, arr, low, high, beat_id):
    pivot = arr[high]
    tracer.set_active_range("main", low, high, f"active range {low}..{high}", beat_id)
    tracer.set_note(f"Partition {low}..{high}; pivot = {pivot}", beat_id)
    tracer.create_pointer("p_i", "i", "main", low - 1, beat_id, position="bottom")
    tracer.create_pointer("p_j", "j", "main", low, beat_id, position="top")
    tracer.create_pointer("p_pivot", "pivot", "main", high, beat_id, position="bottom")
    tracer.highlight("main", [high], "ORANGE", beat_id)
    return low - 1


def finish_partition(tracer, arr, i, high, beat_id):
    pivot_index = i + 1
    tracer.set_note(f"Move pivot into index {pivot_index}", beat_id)
    tracer.highlight("main", [pivot_index, high], "ORANGE", beat_id)
    if pivot_index != high:
        tracer.swap("main", pivot_index, high, beat_id)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    tracer.move_pointer("p_pivot", "main", pivot_index, beat_id)
    tracer.unhighlight("main", [high], beat_id)
    tracer.mark_sorted("main", [pivot_index], beat_id)
    tracer.remove_pointer("p_i", beat_id)
    tracer.remove_pointer("p_j", beat_id)
    tracer.remove_pointer("p_pivot", beat_id)
    tracer.clear_active_range("main", beat_id)
    return pivot_index


def quick_sort_trace():
    tracer = AlgorithmTracer()
    arr = list(DATA)

    tracer.set_note("Quick Sort with rightmost pivots", "beat-001")
    tracer.create_array("main", arr, "beat-001")

    i = start_partition(tracer, arr, 0, 6, "beat-002")
    for j in [0, 1, 2]:
        i = compare_and_maybe_move(tracer, arr, i, j, 6, "beat-003")
    i = compare_and_maybe_move(tracer, arr, i, 3, 6, "beat-004")
    for j in [4, 5]:
        i = compare_and_maybe_move(tracer, arr, i, j, 6, "beat-005")
    finish_partition(tracer, arr, i, 6, "beat-006")

    i = start_partition(tracer, arr, 0, 2, "beat-007")
    for j in [0, 1]:
        i = compare_and_maybe_move(tracer, arr, i, j, 2, "beat-007")
    finish_partition(tracer, arr, i, 2, "beat-007")

    i = start_partition(tracer, arr, 0, 1, "beat-008")
    i = compare_and_maybe_move(tracer, arr, i, 0, 1, "beat-008")
    finish_partition(tracer, arr, i, 1, "beat-009")
    tracer.set_active_range("main", 1, 1, "base case 1..1", "beat-009")
    tracer.set_note("Single value 20 is already fixed", "beat-009")
    tracer.mark_sorted("main", [1], "beat-009")
    tracer.clear_active_range("main", "beat-009")

    i = start_partition(tracer, arr, 4, 6, "beat-010")
    for j in [4, 5]:
        i = compare_and_maybe_move(tracer, arr, i, j, 6, "beat-010")
    finish_partition(tracer, arr, i, 6, "beat-011")

    i = start_partition(tracer, arr, 5, 6, "beat-012")
    i = compare_and_maybe_move(tracer, arr, i, 5, 6, "beat-012")
    finish_partition(tracer, arr, i, 6, "beat-012")
    tracer.set_active_range("main", 5, 5, "base case 5..5", "beat-012")
    tracer.set_note("Single value 70 is already fixed", "beat-012")
    tracer.mark_sorted("main", [5], "beat-012")
    tracer.clear_active_range("main", "beat-012")

    tracer.set_note("Sorted ascending: 10, 20, 30, 40, 50, 70, 90", "beat-013")
    tracer.set_active_range("main", 0, 6, "final sorted array", "beat-013")
    tracer.mark_sorted("main", list(range(len(arr))), "beat-013")
    tracer.clear_active_range("main", "beat-013")

    if arr != sorted(DATA):
        raise RuntimeError(f"Trace ended with {arr}, expected {sorted(DATA)}")

    tracer.output()


if __name__ == "__main__":
    quick_sort_trace()

