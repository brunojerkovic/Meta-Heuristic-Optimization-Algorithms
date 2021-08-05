import numpy as np

from Problem.Problem import Problem


class ProblemTSP(Problem):
    def read_file(self, filename):
        cnt = 0

        with open(filename) as f:
            for i, line in enumerate(f.readlines()):
                # Read problem's metadata
                if line.startswith('NAME'):
                    self.problem_name = line.split(':')[1].strip()
                elif line.startswith('DIMENSION'):
                    map_dimension = int(line.split(':')[1])
                    self.cities = np.zeros(shape=(map_dimension, 2))  # This is to add the coords and indexes of the items of this city
                    self.map_dimension = map_dimension
                elif line[0].isdigit():
                    self.cities[cnt] = np.array([float(line.split()[0]), float(line.split()[1])])
                    cnt += 1

    def get_distances(self):
        map = self.cities
        if not hasattr(self, 'distances'):
            self.distances = np.array([[DistanceFunctions.euclidian_distance(map_city1, map_city2) for map_city1 in map] for map_city2 in map])
        return self.distances

class DistanceFunctions:
    @staticmethod
    def euclidian_distance(city1, city2):
        return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5