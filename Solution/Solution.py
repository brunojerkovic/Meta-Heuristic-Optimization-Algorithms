from dataclasses import dataclass

@dataclass(
    init=True,
    repr=True,
    eq=True,
    order=False
)
class Solution:
    problem_name: str = ''
    fit: float = 0.