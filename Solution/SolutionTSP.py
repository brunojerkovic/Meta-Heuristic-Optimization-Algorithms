from Solution.Solution import Solution
from Problem.ProblemTSP import ProblemTSP
import numpy as np


class SolutionTSP(Solution):

    def __init__(self, problem: ProblemTSP, permute_cities=False):
        self.problem = problem
        self.cities = np.arange(problem.map_dimension)
        if permute_cities:
            self.cities = np.random.permutation(self.cities)
        self.map_dimension = problem.map_dimension
        self.evaluate() # Evaluate the randomly generated solution

    @staticmethod
    def euclidian_distance(x1, x2, y1, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5

    def evaluate(self):
        distance = 0.
        for c1, c2 in zip(self.cities, self.cities[1:]):
            distance += SolutionTSP.euclidian_distance(self.problem.cities[c1][0], self.problem.cities[c2][0], self.problem.cities[c1][1], self.problem.cities[c2][1])

        start_city = self.cities[0]
        end_city = self.cities[-1]
        distance += SolutionTSP.euclidian_distance(self.problem.cities[end_city][0], self.problem.cities[start_city][0], self.problem.cities[end_city][1], self.problem.cities[start_city][1])

        self.fit = -1 * distance

    def __str__(self):
        return f'Cities: {self.cities}\n Map dimension: {self.map_dimension}\n Fit: {self.fit}'

    def add_attribute(self, attr):
        setattr(self, attr, attr)
