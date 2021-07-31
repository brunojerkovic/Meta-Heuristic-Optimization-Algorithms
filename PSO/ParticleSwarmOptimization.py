import numpy as np
from OptimizationAlgorithm import OptimizationAlgorithm
from Solution.SolutionTSP import SolutionTSP
import random

class ParticleSwarmOptimization(OptimizationAlgorithm):
    def __init__(self, pop_size, n_dim, max_iter):
        self.pop_size = pop_size
        self.n_dim = n_dim
        self.max_iter = max_iter

    def solve(self, problem, progressbar = None):
        solution = SolutionTSP(problem=problem)
        pop_size = self.pop_size
        n_dim = self.n_dim
        max_iter = self.max_iter


        # Algorithm
        for i in range(pop_size):
            for d in range(n_dim):
                position[i][d] = random.randint(position_min[d], position_max[d])
                velocity[i][d] = random.randint(velocity_min[d], velocity_max[d])


        for i in range(max_iter):
            for i in range(pop_size):
                pop[i].evaluate()

            # Does the particle have its own better solution?
            for i in range(pop_size):
                if pop[i].fit > p_best[i]:
                    pbest[i] = pop[i] # Copy position and fit

            # Is there globally a better solution now?

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
