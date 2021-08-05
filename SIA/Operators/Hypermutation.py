import numpy as np
import random
from functools import wraps
from Solution.SolutionTSP import SolutionTSP


class HypermutationDecorators:
    @staticmethod
    def extract_dec(hypermutation_fn):
        @wraps(hypermutation_fn)
        def inner(solution, problem, best_fit, c):
            mutated_solution = SolutionTSP(problem=problem)
            mutated_solution.cities = hypermutation_fn(solution.cities, solution.fit, best_fit, c)
            mutated_solution.evaluate()
            return mutated_solution
        return inner

class Hypermutation:
    @staticmethod
    @HypermutationDecorators.extract_dec
    def static_mutation(cities, fit, best_fit, c):
        for _ in range(int(c)):
            a = random.randint(0, len(cities)-1)
            b = random.randint(0, len(cities)-1)
            aux = cities[a]
            cities[a] = cities[b]
            cities[b] = aux
        return cities

    @staticmethod
    @HypermutationDecorators.extract_dec
    def proportional_mutation(cities, fit, best_fit, c):
        c = int((best_fit - fit) * c) if best_fit != np.inf * -1 else 2.0
        for _ in range(int(c)):
            a = random.randint(0, len(cities) - 1)
            b = random.randint(0, len(cities) - 1)
            aux = cities[a]
            cities[a] = cities[b]
            cities[b] = aux
        return cities

    @staticmethod
    @HypermutationDecorators.extract_dec
    def inversely_proportional_mutation(cities, fit, best_fit, c):
        c = int((1 - best_fit/fit) * c) if best_fit != np.inf * -1 else 2.0
        for _ in range(int(c)):
            a = random.randint(0, len(cities) - 1)
            b = random.randint(0, len(cities) - 1)
            aux = cities[a]
            cities[a] = cities[b]
            cities[b] = aux
        return cities