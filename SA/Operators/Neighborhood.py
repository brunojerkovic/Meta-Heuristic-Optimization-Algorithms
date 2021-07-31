import random
import numpy as np


class Neighborhood:
    @staticmethod
    def generate_neighbor(solution):
        ind1 = random.randint(0, len(solution.cities))
        el = solution.cities[ind1]
        ind2 = np.where(solution.cities == el)

        # Swap elements
        solution.cities[ind1] = solution.cities[ind2]
        solution.cities[ind2] = el
        return solution