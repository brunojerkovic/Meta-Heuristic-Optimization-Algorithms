import numpy as np
from SimulatedAnnealing import SA

class GUI:
    def __init__(self, master_frame, position=(0,0)):
        self.master_frame = master_frame
        self.position = position

        # region Parameters
        self.cooling_plan = None
        self.start_temp = None
        self.M = None
        self.termination_condition = None
        # endregion

    def run_algorithm(self, progressbar):
        sa = SA(cooling_plan=self.cooling_plan, start_temp=self.start_temp, M=self.M, termination_condition=self.termination_condition)
        solutions = sa.solve(progressbar)
        return solutions[0]
