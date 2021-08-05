import random
from functools import wraps
import numpy as np
from Solution.SolutionTSP import SolutionTSP

class NeighborhoodDecorators:
    @staticmethod
    def extract_dec(neighborhood_fn):
        @wraps(neighborhood_fn)
        def inner(solution, problem):
            mutated_solution = SolutionTSP(problem=problem)
            mutated_solution.cities = neighborhood_fn(solution.cities)
            mutated_solution.evaluate()
            return mutated_solution

        return inner

class Neighborhood:
    @staticmethod
    @NeighborhoodDecorators.extract_dec
    def insertion(cities):
        '''
        :param cities: list of cities
        :return: neighboring list of cities
        '''
        # Take random element
        ind_take = random.randint(0, len(cities) - 1)
        element = cities[ind_take]
        neighbor_cities = np.concatenate((cities[:ind_take], cities[(ind_take+1):]))

        # Put element at random location
        ind_put = random.randint(0, len(neighbor_cities)+1) # +1 because it can go at the end (dont forget that len of offspring is now smaller by 1)
        neighbor_cities = np.concatenate((neighbor_cities[:ind_put], [element], neighbor_cities[ind_put:]))

        return neighbor_cities

