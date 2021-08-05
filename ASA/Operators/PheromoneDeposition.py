from functools import wraps
import numpy as np
import copy
from Solution.SolutionTSP import SolutionTSP
from Problem.ProblemTSP import DistanceFunctions


class PheromoneDepositionDecorators:
    @staticmethod
    def extract_dec(pheromone_deposition_fn):
        @wraps(pheromone_deposition_fn)
        def inner(tau, solutions, problem):
            cities = [solution.cities for solution in solutions]
            tau = pheromone_deposition_fn(tau, cities, problem.cities)
            return tau
        return inner

class PheromoneDeposition:
    @staticmethod
    @PheromoneDepositionDecorators.extract_dec
    def ant_system_update(tau, paths, map):
        # Update pheromones on every path
        for path in paths:
            for from_city, to_city in zip(path, path[1:]):
                tau[from_city][to_city] += 1 / DistanceFunctions.euclidian_distance(city1=map[from_city], city2=map[to_city])
        return tau

    @staticmethod
    @PheromoneDepositionDecorators.extract_dec
    def elitist_ant_system_update(tau, paths, map):
        m = len(paths)

        # Update pheromones on every path
        for path in paths:
            for from_city, to_city in zip(path, path[1:]):
                tau[from_city][to_city] += 1 / DistanceFunctions.euclidian_distance(city1=map[from_city],city2=map[to_city])

        # Elitist version addition
        best_path = paths[0]
        for from_city, to_city in zip(best_path, best_path[1:]):
            tau[from_city][to_city] += m * 1 / DistanceFunctions.euclidian_distance(city1=map[from_city], city2=map[to_city])

        return tau

    @staticmethod
    @PheromoneDepositionDecorators.extract_dec
    def rank_based_ant_system_update(tau, paths, map):
        m = len(paths)

        # Update pheromones on every path
        for path in paths:
            for k, (from_city, to_city) in enumerate(zip(path, path[1:])):
                tau[from_city][to_city] += (m - k) * 1 / DistanceFunctions.euclidian_distance(city1=map[from_city],city2=map[to_city])

        # Elitist version addition
        best_path = paths[0]
        for from_city, to_city in zip(best_path, best_path[1:]):
            tau[from_city][to_city] += m * 1 / DistanceFunctions.euclidian_distance(city1=map[from_city], city2=map[to_city])

        return tau