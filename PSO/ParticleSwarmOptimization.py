import numpy as np
from OptimizationAlgorithm import OptimizationAlgorithm
from Solution.SolutionTSP import SolutionTSP
import random
from PSO.Operators.VelocityUpdate import VelocityUpdate
from PSO.Operators.UpdatePosition import UpdatePosition


class ParticleSwarmOptimization(OptimizationAlgorithm):
    def __init__(self, pop_size, min_vel, max_vel, iter_num, velocity_update_fn):
        self.pop_size = pop_size
        self.min_vel = min_vel
        self.max_vel = max_vel
        self.iter_num = iter_num
        self.velocity_update_fn = velocity_update_fn

    def solve(self, problem):
        pop_size = self.pop_size
        min_vel = self.min_vel
        max_vel = self.max_vel
        iter_num = self.iter_num
        velocity_update_fun = self.velocity_update_fn

        # Instantiate globally best solution
        g_best_fit = -1 * np.inf
        g_best_position = []

        # Instantiate solutions
        solutions = [SolutionTSP(problem=problem, permute_cities=True) for _ in range(pop_size)]

        # Add properties to the Solution class for position and velocity
        for solution in solutions:
            solution.add_attribute('velocity')
            solution.add_attribute('p_best_fit')
            solution.p_best_fit = -1 * np.inf
            solution.add_attribute('p_best_position')

        # Instantiate velocity
        for solution in solutions:
            solution.velocity = random.randint(min_vel, max_vel)

        for _ in range(iter_num):
            # Evaluate population
            for solution in solutions:
                solution.evaluate()

            # Update p_best for all solutions in population
            for solution in solutions:
                if solution.fit > solution.p_best_fit:
                    solution.p_best_fit = solution.fit
                    solution.p_best_cities = solution.cities

            # Update g_best for all solutions in population
            for solution in solutions:
                if solution.fit > g_best_fit:
                    g_best_fit = solution.fit
                    g_best_position = solution.cities

            # Update position and velocity of each solution
            for solution in solutions:
                velocity = VelocityUpdate.stable_velocity_update(solution.velocity, solution.cities, solution.p_best_cities, g_best_position)
                velocity = int(min(velocity))

                solution.cities = UpdatePosition.swap_operator(velocity, solution.cities)

        # Create the solution from the globally best one
        best_solution = SolutionTSP(problem=problem)
        best_solution.cities = g_best_position
        best_solution.evaluate()

        return [best_solution]
