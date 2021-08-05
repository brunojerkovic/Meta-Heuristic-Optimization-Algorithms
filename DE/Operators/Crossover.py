import random

import numpy as np
from functools import wraps
from Solution.SolutionTSP import SolutionTSP

class CrossoverDecorators:
    @staticmethod
    def extract_dec(crossover_fn):
        @wraps(crossover_fn)
        def inner(solution_target, solution_mutant, problem, Cr):
            solution_trial = SolutionTSP(problem=problem)
            solution_trial.cities = crossover_fn(solution_target.cities, solution_mutant.cities, Cr)
            return solution_trial
        return inner

class Crossover:
    @staticmethod
    @CrossoverDecorators.extract_dec
    def exponential_crossover(cities_target, cities_mutant, Cr):
        cities_trial = np.arange(len(cities_target))
        start = random.randint(0, len(cities_trial))
        indices = np.concatenate([np.arange(start, len(cities_mutant)), np.arange(0, start)])

        from_mutant = True
        for i in indices:
            if from_mutant and random.random() > Cr:
                from_mutant = False

            if from_mutant:
                cities_trial[i] = cities_mutant[i]
            else:
                cities_trial[i] = cities_target[i]

        return cities_trial

    @staticmethod
    @CrossoverDecorators.extract_dec
    def uniform_crossover(cities_target, cities_mutant, Cr):
        cities_trial = np.arange(len(cities_target))
        start = random.randint(0, len(cities_trial))
        indices = np.concatenate([np.arange(start, len(cities_mutant)), np.arange(0, start)])

        for i in indices:
            if random.random() < Cr:
                cities_trial[i] = cities_mutant[i]
            else:
                cities_trial[i] = cities_target[i]

        return cities_trial