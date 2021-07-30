import numpy as np

from Problem.Problem import Problem


class ProblemTSP(Problem):
    def __init__(self, cities, problem_name, map_dimension):
        pass

    def read_file(self, filename):
        cnt = 0

        with open(filename) as f:
            for i, line in enumerate(f.readlines()):
                # Read problem's metadata
                if line.startswith('NAME'):
                    super.problem_name = line.split(':')[1].strip()
                elif line.startswith('DIMENSION'):
                    map_dimension = (int(line.split(':')[1]), 2)
                    self.cities = np.zeros(shape=(map_dimension, 2))  # This is to add the coords and indexes of the items of this city
                    self.map_dimension = map_dimension
                elif line.startswith('NODE_COORD_SECTION'):
                    self.cities[cnt] = np.array([*float(line.split())])
                    cnt += 1