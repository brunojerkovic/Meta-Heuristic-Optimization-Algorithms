import numpy as np
import copy
import random


class UpdatePosition:
    @staticmethod
    def swap_operator(velocity, position):
        new_position = copy.deepcopy(position)
        for _ in range(velocity):
            a = random.randint(0, len(position)-1)
            b = random.randint(0, len(position)-1)
            aux = new_position[a]
            new_position[a] = new_position[b]
            new_position[b] = aux
        return new_position


