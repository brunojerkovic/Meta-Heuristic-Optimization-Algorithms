import numpy as np
from OptimizationAlgorithm import OptimizationAlgorithm
from Solution.SolutionTSP import SolutionTSP
import copy

class SimpleImmunologicalAlgorithm(OptimizationAlgorithm):
    def __init__(self, hypermutation_fn, hypermutation_constant, pop_size, iter_num, dup_num):
        self.hypermutation_fn = hypermutation_fn
        self.hypermutation_constant = hypermutation_constant
        self.pop_size = pop_size
        self.iter_num = iter_num
        self.dup_num = dup_num

    def solve(self, problem):
        hypermutation_fn = self.hypermutation_fn
        hypermutation_constant = self.hypermutation_constant
        pop_size = self.pop_size
        iter_num = self.iter_num
        dup_num = self.dup_num

        # Instantiate global fit
        g_best_fit = -1 * np.inf

        # Instantiate solutions
        solutions = [SolutionTSP(problem=problem, permute_cities=True) for _ in range(pop_size)]

        # Evaluate instantiated population
        for solution in solutions:
            solution.evaluate()

        for _ in range(iter_num):
            # Clone each element dupl times
            p_clo = []
            for solution in solutions:
                p_clo += [copy.deepcopy(solution) for _ in range(dup_num)]

            # Hypermutate p_clo
            mutated_p_clo = [hypermutation_fn(dup_sol, problem, g_best_fit, hypermutation_constant) for dup_sol in solutions]

            # Evaluate p_clo
            for m_dup_sol in mutated_p_clo:
                m_dup_sol.evaluate()

            # Select best 'pop_size' solutions
            sorted_solutions = sorted(solutions+mutated_p_clo, key=lambda sol: sol.fit, reverse=True)
            solutions = sorted_solutions[:pop_size]

            # Update best fit
            g_best_fit = solutions[0].fit if solutions[0].fit > g_best_fit else g_best_fit

        return [solutions[0]]
