import random
from functools import wraps
import copy

class CloningDecorators:
    @staticmethod
    def extract_dec(cloning_fn):
        @wraps(cloning_fn)
        def inner(solutions, dup_num):
            sorted_solutions = sorted(solutions, key=lambda sol: sol.fit, reverse=True)
            cloned_solutions = cloning_fn(sorted_solutions, dup_num)
            for solution in cloned_solutions:
                solution.evaluate()
            return cloned_solutions
        return inner

class Cloning:
    @staticmethod
    @CloningDecorators.extract_dec
    def static_cloning_operator(solutions, dup_num):
        # Clone each element dup times
        p_clo = []
        for solution in solutions:
            p_clo += [copy.deepcopy(solution) for _ in range(dup_num)]
        return p_clo

    @staticmethod
    @CloningDecorators.extract_dec
    def proportional_cloning_operator(solutions, dup_num):
        p_clo = []
        for i, solution in enumerate(solutions):
            p_clo += [copy.deepcopy(solution) for _ in range(dup_num * (i+1))]
        return p_clo