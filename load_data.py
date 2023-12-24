INVALID_FILE_FORMAT_MESSAGE = """Input file invalid:
File should match rules:
1) First line is size n of n x n matrix A 
2) Following lines are corresponding n rows of matrix A
3) Last line is transposed vector y
4) All lines are separated with '\\n' (newline symbol) 
"""


class FileValidationException(Exception):
    pass


def validate_input(n: int, matrix_rows: list[list[float]], vector: list[float]) -> None:
    if len(matrix_rows) != n or not all(
        (len(row) == n for row in [*matrix_rows, vector])
    ):
        raise FileValidationException()


def transform_input(
    n: str, matrix_rows: list[str], vector: str
) -> tuple[int, list[list[float]], list[float]]:
    n = int(n)
    matrix_rows = list(
        map(lambda x: [float(number) for number in x.split(" ")], matrix_rows)
    )
    vector = [float(number) for number in vector.split(" ")]

    validate_input(n, matrix_rows, vector)

    return n, matrix_rows, vector


def extract_gauss_parameters(
    input_data: str,
) -> tuple[int, list[list[float]], list[float]]:
    try:
        n, *matrix_rows, vector = input_data.strip().split("\n")
        return transform_input(n, matrix_rows, vector)
    except (ValueError, FileValidationException) as e:
        print(INVALID_FILE_FORMAT_MESSAGE)
        raise


def load_data_from_file(filepath: str) -> tuple[int, list[list[float]], list[float]]:
    with open(filepath) as file:
        data = file.read()
    return extract_gauss_parameters(data)
