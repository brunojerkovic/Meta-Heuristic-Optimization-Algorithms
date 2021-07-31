import tkinter as tk
import os
from SA.SimulatedAnnealing import SA
from AlgorithmGUI import AlgorithmGUI
from SA.Operators.CoolingPlan import CoolingPlan

class GUI(AlgorithmGUI):
    def __init__(self, problem, master_frame, filename, position=(0,0)):
        self.master_frame = master_frame
        self.problem = problem
        self.filename = filename

        # region Hyperparameters
        self.hyperparameters_frame = tk.LabelFrame(self.master_frame, text='HYPERPARAMETERS', padx=5, pady=5)
        self.hyperparameters_frame.grid(row=position[0], column=position[1], columnspan=2)

        # Cooling Plan
        tk.Label(self.hyperparameters_frame, fg='black', text='Cooling Plan: ').grid(row=0, column=0)
        cooling_plan_options = [method for method in dir(CoolingPlan) if method.startswith('_') is False]
        cooling_plan_options = GUI.preprocessing_enums_for_option_menu(cooling_plan_options)
        self.cooling_plan_choice = tk.StringVar(self.hyperparameters_frame)
        self.cooling_plan_choice.set(cooling_plan_options[0])
        self.cooling_plan_menu = tk.OptionMenu(self.hyperparameters_frame, self.cooling_plan_choice, *cooling_plan_options)
        self.cooling_plan_menu.grid(row=0, column=1)

        # Starting temperature
        tk.Label(self.hyperparameters_frame, fg='black', text='Starting temperature: ').grid(row=1, column=0)
        self.start_temp_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.start_temp_entry.insert(tk.END, '100')
        self.start_temp_entry.grid(row=1, column=1)

        # M (repetitions per same temperature)
        tk.Label(self.hyperparameters_frame, fg='black', text='M: ').grid(row=2, column=0)
        self.M_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.M_entry.insert(tk.END, '2')
        self.M_entry.grid(row=2, column=1)

        # Iteration Number
        tk.Label(self.hyperparameters_frame, fg='black', text='Iterations per temperature value: ').grid(row=3, column=0)
        self.iter_num_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.iter_num_entry.insert(tk.END, '100')
        self.iter_num_entry.grid(row=3, column=1)

        # Beta
        tk.Label(self.hyperparameters_frame, fg='black', text='Beta value: ').grid(row=4, column=0)
        self.beta_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.beta_entry.insert(tk.END, '0.01')
        self.beta_entry.grid(row=4, column=1)
        # endregion

    def run_algorithm(self, progressbar, save=True):
        cooling_plan_fn = eval('CoolingPlan.' + GUI.preprocessing_option_menu_for_enum(self.cooling_plan_choice.get()))
        start_temp = float(self.start_temp_entry.get())
        M = int(self.M_entry.get())
        iter_num = int(self.iter_num_entry.get())
        beta = float(self.beta_entry.get())

        sa = SA(cooling_plan=cooling_plan_fn, start_temp=start_temp, M=M, iter_num=iter_num, beta=beta)
        solutions = sa.solve(self.problem, progressbar=progressbar)

        if save:
            self.save_results(solutions[0])

        return solutions[0].fit

    def save_results(self, fit):
        # If directories do not exist, create them
        directory = 'Results'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Find out the new name for the file
        onlyfiles = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        file_nums = [int(file.split('.txt')[0]) for file in onlyfiles] if len(onlyfiles) > 0 else [0]
        file_nums.sort()
        new_name = str(file_nums[-1] + 1)
        new_name = new_name if len(new_name) >= 1 else '0' + new_name

        # Save text file
        vals = {
            'Filename: ': self.filename,
            'Algorithm type: ': 'Simulated Annealing',
            'Cooling Plan: ': self.cooling_plan_choice.get(),
            'Starting temperature': self.start_temp_entry.get(),
            'M': self.M_entry.get(),
            'Iteration number: ': self.iter_num_entry.get(),
            'Fit: ': fit

        }
        with open(f'{directory}/{new_name}.txt', 'w+') as f:
            for key, val in zip(list(vals.keys()), list(vals.values())):
                f.write(f'{key}={val}\n_')
        print("Results saved")
