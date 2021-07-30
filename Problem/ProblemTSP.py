from Problem.Problem import Problem


class ProblemTSP(Problem):
    def __init__(self, cities, problem_name, map_dimension):
        self.cities = cities
        self.problem_name = problem_name
        self.map_dimension = map_dimension

    def read_file(self):
        pass