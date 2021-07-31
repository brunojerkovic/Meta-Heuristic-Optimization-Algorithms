import numpy as np

class CoolingPlan:
    @staticmethod
    def linear_cooling_plan(T0, k, beta):
        return T0 - k * beta

    @staticmethod
    def geom_cooling_plan(T0, k, beta):
        return T0 * (beta ** k)

    @staticmethod
    def log_cooling_plan(T0, k):
        return T0 / np.log(k)

    @staticmethod
    def slow_cooling_plan(T0, k, beta):
        Tk = T0
        for _ in range(k):
            Tk /= (1 + beta * Tk)
        return Tk
