from dataclasses import dataclass
import abc

@dataclass(
    init=True,
    repr=True,
    eq=True,
    order=False
)
class Problem(metaclass=abc.ABCMeta):
    problem_name: str = ''

    @abc.abstractmethod
    def read_file(self):
        pass
