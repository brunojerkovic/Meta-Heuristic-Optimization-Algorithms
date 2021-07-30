from Solution.Solution import Solution


class SolutionTSP(Solution):
    def __init__(self, cities, problem_name, map_dimension):
        self.cities = cities
        self.problem_name = problem_name
        self.map_dimension = map_dimension

    # TODO: implement function
    @staticmethod
    def generate_random_solution():
        pass