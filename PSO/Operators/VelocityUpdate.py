import numpy as np
import random
from functools import wraps
from Solution.SolutionTSP import SolutionTSP


class VelocityUpdate:
    @staticmethod
    def vanilla_velocity_update(v_prev, x, p_best, g_best, c1=2., c2=2.):
        return v_prev + c1 * random.random() * (p_best - x) + c2 * random.random() * (g_best - x)

    @staticmethod
    def itertion_velocity_update(v_prev, x, p_best, g_best, c1=2., c2=2., w = 0.9):
        return w * v_prev + c1 * random.random() * (p_best - x) + c2 * random.random() * (g_best - x)

    @staticmethod
    def itertion_velocity_update_adaptive_control(v_prev, x, p_best, g_best, iter_num, T, c1=2., c2=2., w_max=1, w_min=0.9):
        w = iter_num / T * (w_max - w_min) + w_max if iter_num <= T else w_min
        return w * v_prev + c1 * random.random() * (p_best - x) + c2 * random.random() * (g_best - x)

    @staticmethod
    def stable_velocity_update(v_prev, x, p_best, g_best, c1=2.05, c2=2.05):
        phi = c1 + c2
        K = 2 / (np.abs(2 - phi - np.sqrt(phi**2 - 4 * phi)))
        return K * (v_prev + c1 * random.random() * (p_best - x) + c2 * random.random() * (g_best - x))