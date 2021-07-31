import numpy as np
from OptimizationAlgorithm import OptimizationAlgorithm
from Solution.SolutionTSP import SolutionTSP
from Operators.Neighborhood import Neighborhood
import random

class SA(OptimizationAlgorithm):
    def __init__(self, cooling_plan, start_temp, M, iter_num):
        self.cooling_plan = cooling_plan
        self.start_temp = start_temp
        self.M = M
        self.iter_num = iter_num

    def solve(self, problem, progressbar = None):
        solution_curr = SolutionTSP(problem=problem)
        cool_plan = self.cooling_plan
        temp = self.start_temp
        M = self.M
        iter_num = self.iter_num
        alpha, beta = 1., 1.

        # Algorithm
        for k in range(1, iter_num):
            temp = cool_plan(temp, k, alpha)
            for _ in range(M):
                neighbor = Neighborhood.generate_neighbor(solution_curr)
                delta = neighbor.fit - solution_curr.fit
                if delta <= 0: # Accepts if it is equal just to add diversity
                    solution_curr = neighbor
                else:
                    solution_curr = neighbor if random.random() < np.exp(-delta/temp) else solution_curr

        return None
