import numpy as np
from OptimizationAlgorithm import OptimizationAlgorithm
from Solution.SolutionTSP import SolutionTSP
import copy

class ClonAlg(OptimizationAlgorithm):
    def __init__(self, cloning_fn, hypermutation_fn, hypermutation_constant, pop_size, iter_num, dup_num):
        self.cloning_fn = cloning_fn
        self.hypermutation_fn = hypermutation_fn
        self.hypermutation_constant = hypermutation_constant
        self.pop_size = pop_size
        self.iter_num = iter_num
        self.dup_num = dup_num

    def solve(self, problem, progressbar = None):
        hypermutation_fn = self.hypermutation_fn
        hypermutation_constant = self.hypermutation_constant
        pop_size = self.pop_size
        iter_num = self.iter_num
        cloning_fn = self.cloning_fn
        dup_num = self.dup_num

        # Instantiate global fit
        g_best_fit = -1 * np.inf

        # Instantiate solutions
        solutions = [SolutionTSP(problem=problem, permute_cities=True) for _ in range(pop_size)]

        # Evaluate instantiated population
        for solution in solutions:
            solution.evaluate()

        for _ in range(iter_num):
            # Evaluate population
            for solution in solutions:
                solution.evaluate()

            # Clone population
            p_clo = cloning_fn(solutions, dup_num)

            # Hypermutate p_clo
            p_hyp = [hypermutation_fn(dup_sol, problem, g_best_fit, hypermutation_constant) for dup_sol in p_clo]

            # Evaluate hypermutated population
            for sol in p_hyp:
                sol.evaluate()

            # Sort p_hyp
            sorted_p_hyp = sorted(p_hyp, key=lambda sol: sol.fit, reverse=True)

            # Create new antibodies
            p_birth = [SolutionTSP(problem=problem, permute_cities=True) for _ in range(dup_num)]

            # Replace the worst antibodies with the new ones
            solutions = sorted_p_hyp[:dup_num] + p_birth

            # Select pop_size solutions
            sorted_solutions = sorted(solutions, key=lambda sol: sol.fit, reverse=True)
            solutions = sorted_solutions[:pop_size]

            # Update best fit
            g_best_fit = solutions[0].fit if solutions[0].fit > g_best_fit else g_best_fit

        return [solutions[0]]
