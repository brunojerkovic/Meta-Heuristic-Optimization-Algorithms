import random
from functools import wraps
from Solution.SolutionTSP import SolutionTSP
import numpy as np

class MutationDecorators:
    @staticmethod
    def extract_dec(mutation_fn):
        @wraps(mutation_fn)
        def inner(population, num_lin_comb, problem):
            mutant_solutions = []
            cities_pop = [s.cities for s in population]

            # Mutate entire population of solutions
            for solution in population:
                mutant_solution = SolutionTSP(problem=problem)
                mutant_solution.cities = mutation_fn(solution.cities, cities_pop, num_lin_comb)
                mutant_solutions.append(mutant_solution)

            return mutant_solutions
        return inner

class Mutation:
    @staticmethod
    @MutationDecorators.extract_dec
    def random_de_mutation(cities_base, cities_pop, num_lin_comb):
        # Select base vector
        mutated_city = np.array(cities_base)

        # Mutate the base vector with the help of 2 other vectors
        for _ in range(num_lin_comb):
            pic1 = random.randint(0, len(cities_pop)-1)
            pic2 = random.randint(0, len(cities_pop)-1)

            mutated_city += (cities_pop[pic1] - cities_pop[pic2])

        return mutated_city