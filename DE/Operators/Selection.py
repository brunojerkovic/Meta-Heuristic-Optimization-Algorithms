import random
import numpy as np
from functools import wraps
from Solution.SolutionTSP import SolutionTSP

class SelectionDecorators:
    @staticmethod
    def extract_dec(selection_fn):
        @wraps(selection_fn)
        def inner(target_solutions, trial_solutions):
            new_pop_solutions = selection_fn(target_solutions, trial_solutions)
            return new_pop_solutions
        return inner

class Selection:
    @staticmethod
    @SelectionDecorators.extract_dec
    def simple_pair_selection(target_solutions, trial_solutions):
        random.shuffle(target_solutions)
        random.shuffle(trial_solutions)
        new_pop = []

        for target_solution, trial_solution in zip(target_solutions, trial_solutions):
            new_pop.append(trial_solution) if trial_solution.fit >= target_solution.fit else new_pop.append(target_solution)

        return new_pop