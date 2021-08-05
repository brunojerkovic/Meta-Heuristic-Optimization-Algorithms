import numpy as np
from OptimizationAlgorithm import OptimizationAlgorithm
from Solution.SolutionTSP import SolutionTSP
import copy

class DifferentialEvolution(OptimizationAlgorithm):
    def __init__(self, selection_fn, mutation_fn, crossover_fn, tsp_constraint_solver_fn, pop_size, iter_num, crossover_constant, lin_comb_num):
        self.selection_fn = selection_fn
        self.mutation_fn = mutation_fn
        self.crossover_fn = crossover_fn
        self.tsp_constraint_solver_fn = tsp_constraint_solver_fn
        self.pop_size = pop_size
        self.iter_num = iter_num
        self.crossover_constant = crossover_constant
        self.lin_comb_num = lin_comb_num

    def solve(self, problem):
        selection_fn = self.selection_fn
        mutation_fn = self.mutation_fn
        crossover_fn = self.crossover_fn
        tsp_constraint_solver_fn = self.tsp_constraint_solver_fn
        pop_size = self.pop_size
        iter_num = self.iter_num
        crossover_constant = self.crossover_constant
        lin_comb_num = self.lin_comb_num

        # Instantiate solutions
        solutions = [SolutionTSP(problem=problem, permute_cities=True) for _ in range(pop_size)]

        # Algorithm
        for _ in range(iter_num):
            # Mutate solutions
            mutated_solutions = mutation_fn(solutions, lin_comb_num, problem)

            # Generate trial vectors
            trial_solutions = []
            for solution_target, solution_mutant in zip(solutions, mutated_solutions):
                trial_solutions.append(crossover_fn(solution_target, solution_mutant, problem, crossover_constant))

            # Solve the TSP constraint
            solved_trial_solutions = tsp_constraint_solver_fn(trial_solutions)

            # Select for next population
            solutions = selection_fn(solutions, solved_trial_solutions)

            # Order solutions by fit
            sorted(solutions, key=lambda sol: sol.fit, reverse=True)

        return [solutions[0]]
