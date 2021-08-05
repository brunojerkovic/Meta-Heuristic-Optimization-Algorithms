import numpy as np

from OptimizationAlgorithm import OptimizationAlgorithm
from Solution.SolutionTSP import SolutionTSP
from Problem.ProblemTSP import DistanceFunctions


class AntSystemAlgorithm(OptimizationAlgorithm):
    def __init__(self, alpha, beta, phi, iter_num, pop_size, local_search_fn, pheromone_deposition_fn):
        self.alpha = alpha
        self.beta = beta
        self.phi = phi
        self.iter_num = iter_num
        self.pop_size = pop_size

        self.local_search_fn = local_search_fn
        self.pheromone_deposition_fn = pheromone_deposition_fn

    def solve(self, problem, progressbar=None):
        alpha = self.alpha
        beta = self.beta
        phi = self.phi
        iter_num = self.iter_num
        pop_size = self.pop_size
        local_search_fn = self.local_search_fn
        pheromone_deposition_fn = self.pheromone_deposition_fn

        # Initialize solutions
        init_solutions = [SolutionTSP(problem=problem) for _ in range(pop_size)]

        # Find the initial best solution with local search algorithm
        solutions = []
        cost = 0
        dim = 0
        for i, init_solution in enumerate(init_solutions):
            solution, cost = local_search_fn(init_solution, problem)
            dim = (len(solution.cities))
            solutions.append(solution)

        # Initialize tau, mu, and p
        tau = np.full((dim, dim), pop_size / cost)
        mu = np.array(
            [[1 / DistanceFunctions.euclidian_distance(map_city1, map_city2) for map_city1 in problem.cities] for map_city2
             in problem.cities])
        p = np.ones((dim, dim))

        # Algorithm
        for i in range(iter_num):
            # Create solution for each ant based on probability distribution p (p is prob. of ant going from city i to city j)
            if i != 0:
                for solution in solutions:
                    # Create a solution for an ant
                    new_path = [solution.cities[0]]
                    for city_ind in solution.cities[:-1]:
                        # "Don't go back to where you already were" constraint (remove the "already visited" cities)
                        potential_cities = np.array([c for c in np.arange(0, dim) if c not in new_path])
                        potential_probs = np.array([p[city_ind][c] for c in np.arange(0, dim) if c not in new_path])

                        if np.inf in potential_probs:
                            print("H")

                        # Normalize probs
                        potential_probs /= potential_probs.sum()

                        # Choose the next city
                        if len(potential_cities) > 1:
                            next_city_ind = np.random.choice(potential_cities, p=potential_probs) # This is [0, 30>
                        else:
                            # If there is only one city an ant can go to, it has to go there (there is no probability)
                            next_city_ind = potential_cities[0]
                        new_path.append(next_city_ind)

                    # Update the path for this ant
                    solution.cities = new_path
                    solution.evaluate()

            # Deposit pheromones
            tau = tau * (1 - phi)

            # Order solutions by fit
            sorted(solutions, key=lambda sol: sol.fit, reverse=True)

            # Update pheromone trails
            tau = pheromone_deposition_fn(tau, solutions, problem)

            # Calculate p
            p = np.ones((dim, dim))
            for city_ind, prob_list in enumerate(p):
                for next_city_ind, prob in enumerate(prob_list):
                    denominator = np.array([(t ** alpha) * (n ** beta) for t, n in zip(tau[city_ind], mu[city_ind])])
                    denominator[np.where(denominator == np.inf)[0][0]] = 0
                    denominator = denominator.sum()
                    p[city_ind][next_city_ind] = (tau[city_ind][next_city_ind] ** alpha) * (mu[city_ind][next_city_ind] ** beta) / denominator

                    # Remove the probability of going to the same town in a circle
                    if city_ind == next_city_ind:
                        p[city_ind][next_city_ind] = 0.


        # Order solutions by fit
        sorted(solutions, key=lambda sol: sol.fit, reverse=True)

        return [solutions[0]]
