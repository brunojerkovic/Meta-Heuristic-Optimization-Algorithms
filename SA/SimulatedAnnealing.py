import numpy as np
from OptimizationAlgorithm import OptimizationAlgorithm
from Solution.SolutionTSP import SolutionTSP
from SA.Operators.Neighborhood import Neighborhood
import random

class SimulatedAnnealing(OptimizationAlgorithm):
    def __init__(self, cooling_plan, start_temp, M, iter_num, beta):
        self.cooling_plan = cooling_plan
        self.start_temp = start_temp
        self.M = M
        self.iter_num = iter_num
        self.beta = beta

    def solve(self, problem):
        solution = SolutionTSP(problem=problem)
        cool_plan = self.cooling_plan
        temp = self.start_temp
        M = self.M
        iter_num = self.iter_num
        beta = self.beta

        # Algorithm
        for k in range(1, iter_num):
            temp = cool_plan(temp, k, beta)
            for _ in range(M):
                neighbor = Neighborhood.insertion(solution=solution, problem=problem)
                delta = neighbor.fit - solution.fit
                if delta <= 0: # Accepts if it is equal just to add diversity
                    solution = neighbor
                else:
                    temp = 0.00001 if temp == 0. else round(temp, 5) # Correct if temp == 0
                    solution = neighbor if random.random() < np.exp(-delta/temp) else solution

        return [solution]
