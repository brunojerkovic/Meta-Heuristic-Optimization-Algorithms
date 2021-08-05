import random
import numpy as np
from functools import wraps
import copy

class TSPConstraintSolverDecorators:
    @staticmethod
    def extract_dec(constraint_solver_fn):
        @wraps(constraint_solver_fn)
        def inner(solutions):
            for solution in solutions:
                solution.cities = constraint_solver_fn(solution.cities)
            return solutions
        return inner

class TSPConstraintSolver:
    @staticmethod
    @TSPConstraintSolverDecorators.extract_dec
    def simple_constraint_solver(cities):
        # Round every number to the closest integer
        cities = [int(num) for num in cities]

        # Get missing cities
        missing_city_nums = [c for c in np.arange(len(cities)) if c not in cities]
        missing_ind = 0

        # Fill repeated cities with an element from the missing cities list
        for city_num in set(cities):
            indexes = [i for i, x in enumerate(cities) if x == city_num]
            if len(indexes) > 1:
                for ind in indexes[1:]:
                    cities[ind] = missing_city_nums[missing_ind]
                    missing_ind += 1

        return np.array(cities)