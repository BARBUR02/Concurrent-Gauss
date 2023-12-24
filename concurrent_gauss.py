from graph_processing import (
    calculate_foata_form_groups,
    prepare_dependency_graph,
    print_results,
)
from tasks import A, B, C, Task
from load_data import load_data_from_file
import multiprocessing
import numpy as np

CONFIGURATION_FILE = "input.txt"


def concurrent_gauss(
    shared_matrix: any,
    shared_dict: any,
    n: int,
    task: str,
    barrier: multiprocessing.Event,
) -> None:
    matrix = np.frombuffer(shared_matrix.get_obj()).reshape(
        (n, len(shared_matrix) // n)
    )
    task = Task.parse_from_input(task)
    match task:
        case A():
            shared_dict[task.get_id()] = (
                matrix[task.j - 1, task.i - 1] / matrix[task.i - 1, task.i - 1]
            )
        case B():
            multiplier = shared_dict[f"A[{task.i},{task.k}]"]
            shared_dict[task.get_id()] = multiplier * matrix[task.i - 1, task.j - 1]
        case C():
            matrix[task.k - 1, task.j - 1] -= shared_dict[
                task.get_id().replace("C", "B")
            ]
        case _:
            pass
    barrier.set()


def generate_graph_and_run_gauss() -> np.ndarray:
    n, A_matrix, y = load_data_from_file(CONFIGURATION_FILE)
    dependencies_graph = prepare_dependency_graph(n)
    foata_groups = calculate_foata_form_groups(dependencies_graph)
    print_results(dependencies_graph, foata_groups)
    A_matrix = np.array(A_matrix, dtype="float64")
    y = np.array(y, dtype="float64")
    work_matrix = np.column_stack((A_matrix, y))

    with multiprocessing.Manager() as manager:
        shared_matrix = multiprocessing.Array("d", work_matrix.flatten())
        shared_dict = manager.dict()
        for group in foata_groups:
            barrier = manager.Event()

            processes = []
            for task in group:
                process = multiprocessing.Process(
                    target=concurrent_gauss,
                    args=(shared_matrix, shared_dict, n, task, barrier),
                )
                processes.append(process)
                process.start()

            # Wait for all processes in the group to finish
            for process in processes:
                process.join()

            # Wait for the barrier to be set by all processes
            barrier.wait()
        result = np.frombuffer(shared_matrix.get_obj()).reshape(
            (n, len(shared_matrix) // n)
        )
    return work_matrix, result


if __name__ == "__main__":
    original_M, transformed_M = generate_graph_and_run_gauss()
    print(
        f"Original matrix from input:\n{original_M}\nTransformed matrix:\n{transformed_M}"
    )
