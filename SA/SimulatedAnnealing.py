import numpy as np
from OptimizationAlgorithm import OptimizationAlgorithm
from Solution.SolutionTSP import SolutionTSP

class SA(OptimizationAlgorithm):
    def __init__(self, cooling_plan, start_temp, M, iter_num):
        self.cooling_plan = cooling_plan
        self.start_temp = start_temp
        self.M = M
        self.iter_num = iter_num

    def solve(self, problem, progressbar = None):
        solution = SolutionTSP(problem=problem)
        k = 0
        cool_plan = self.cooling_plan
        start_temp = self.start_temp
        M = self.M
        iter_num = self.iter_num

        #for i in range(1, M[]):
        #    if termination_conditions
        #    for j in range(1, M[i]):
        #        pass
            # generate N(rjesenje)
            # calc difference
            # if it is better solution, accept it
            # else do some calc

        return None
