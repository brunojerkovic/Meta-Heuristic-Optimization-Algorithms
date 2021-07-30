import numpy as np
from OptimizationAlgorithm import OptimizationAlgorithm
from Solution.SolutionTSP import SolutionTSP

class SA(OptimizationAlgorithm):
    def __init__(self, cooling_plan, start_temp, M, termination_condition):
        self.cooling_plan = cooling_plan
        self.start_temp = start_temp
        self.M = M
        self.termination_condition = termination_condition

    def solve(self, progressbar = None):
        solution = SolutionTSP.generate_random_solution()
        k = 0
        cool_plan = self.cooling_plan
        start_temp = self.start_temp
        M = self.M
        termination_condition = self.termination_condition

        #for i in range(1, M[]):
        #    if termination_conditions
        #    for j in range(1, M[i]):
        #        pass
            # generate N(rjesenje)
            # calc difference
            # if it is better solution, accept it
            # else do some calc

        return None
