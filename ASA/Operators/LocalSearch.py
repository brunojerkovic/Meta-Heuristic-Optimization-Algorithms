from functools import wraps
import numpy as np
import copy
from Solution.SolutionTSP import SolutionTSP
from Problem.ProblemTSP import DistanceFunctions


class LocalSearchDecorators:
    @staticmethod
    def extract_dec(local_search_fn):
        @wraps(local_search_fn)
        def inner(initial_solution, problem):
            initial_solution.cities, total_distance = local_search_fn(initial_solution.cities, problem)
            initial_solution.evaluate()
            return initial_solution, total_distance
        return inner

class LocalSearch:
    @staticmethod
    @LocalSearchDecorators.extract_dec
    def perform_nearest_neighbor(path, problem):
        # Calculate total distance
        total_distance = 0

        # Instantiate a new path where you will save the Local Search results
        new_path = np.arange(len(path))
        new_path.fill(-1)

        # Create a matrix of all neighboring distances
        distances = copy.deepcopy(problem.get_distances())

        # Start the new path with a city from which the input list starts (and remove it from the copy of the map)
        new_path[0] = path[0]
        distances[:, new_path[0]] = np.inf
        i = -1

        # Start path from one city
        for _ in range(len(new_path)-1):
            i += 1
            new_path[i+1] = distances[new_path[i]].argmin()
            total_distance += distances[i].min()
            distances[:, new_path[i+1]] = np.inf

        return new_path, total_distance