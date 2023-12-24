from abc import ABC, abstractmethod
import re


class Task(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def parse_task(input: str) -> "Task":
        pass

    @staticmethod
    def parse_from_input(input: str) -> "Task":
        match (input[0]):
            case "A":
                return A.parse_task(input)
            case "B":
                return B.parse_task(input)
            case "C":
                return C.parse_task(input)


class A(Task):
    def __init__(self, i: int, j: int) -> None:
        super().__init__()
        # I add +1 to follow convention from exercises with row numeration starting from 1
        self.i = i + 1
        self.j = j + 1

    def get_id(self) -> str:
        return f"A[{self.i},{self.j}]"

    @staticmethod
    def parse_task(input: str) -> Task:
        digits = [int(digit) - 1 for digit in re.findall(r"\d", input)]
        return A(*digits)

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.get_id() == other.get_id()
        return False

    def __hash__(self):
        return hash(self.get_id())


class B(Task):
    def __init__(self, i: int, j: int, k: int) -> None:
        super().__init__()
        self.i = i + 1
        self.j = j + 1
        self.k = k + 1

    def get_id(self) -> str:
        return f"B[{self.i},{self.j},{self.k}]"

    @staticmethod
    def parse_task(input: str) -> Task:
        digits = [int(digit) - 1 for digit in re.findall(r"\d", input)]
        return B(*digits)

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.get_id() == other.get_id()
        return False

    def __hash__(self):
        return hash(self.get_id())


class C(Task):
    def __init__(self, i: int, j: int, k: int) -> None:
        super().__init__()
        self.i = i + 1
        self.j = j + 1
        self.k = k + 1

    def get_id(self) -> str:
        return f"C[{self.i},{self.j},{self.k}]"

    @staticmethod
    def parse_task(input: str) -> Task:
        digits = [int(digit) - 1 for digit in re.findall(r"\d", input)]
        return C(*digits)

    def __eq__(self, other):
        if isinstance(other, Task):
            return self.get_id() == other.get_id()
        return False

    def __hash__(self):
        return hash(self.get_id())
