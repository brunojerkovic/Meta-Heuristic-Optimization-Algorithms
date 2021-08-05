import tkinter as tk
import os
from AlgorithmGUI import AlgorithmGUI
from DE.Operators.TSPConstraintSolver import TSPConstraintSolver
from DE.Operators.Crossover import Crossover
from DE.Operators.Selection import Selection
from DE.Operators.Mutation import Mutation
from DE.DifferentialEvolution import DifferentialEvolution

class GUI(AlgorithmGUI):
    def __init__(self, problem, master_frame, filename, position=(0,0)):
        self.master_frame = master_frame
        self.problem = problem
        self.filename = filename

        # region Hyperparameters
        self.hyperparameters_frame = tk.LabelFrame(self.master_frame, text='HYPERPARAMETERS', padx=5, pady=5)
        self.hyperparameters_frame.grid(row=position[0], column=position[1], columnspan=2)

        # TSP Constraint Solver
        tk.Label(self.hyperparameters_frame, fg='black', text='TSP Constraint Solver Function: ').grid(row=0, column=0)
        solver_options = [method for method in dir(TSPConstraintSolver) if method.startswith('_') is False]
        solver_options = GUI.preprocessing_enums_for_option_menu(solver_options)
        self.solver_choice = tk.StringVar(self.hyperparameters_frame)
        self.solver_choice.set(solver_options[0])
        self.solver_menu = tk.OptionMenu(self.hyperparameters_frame, self.solver_choice, *solver_options)
        self.solver_menu.grid(row=0, column=1)

        # Crossover function
        tk.Label(self.hyperparameters_frame, fg='black', text='Crossover Function: ').grid(row=1, column=0)
        crossover_options = [method for method in dir(Crossover) if method.startswith('_') is False]
        crossover_options = GUI.preprocessing_enums_for_option_menu(crossover_options)
        self.crossover_choice = tk.StringVar(self.hyperparameters_frame)
        self.crossover_choice.set(crossover_options[0])
        self.crossover_menu = tk.OptionMenu(self.hyperparameters_frame, self.crossover_choice, *crossover_options)
        self.crossover_menu.grid(row=1, column=1)

        # Crossover constant
        tk.Label(self.hyperparameters_frame, fg='black', text='Crossover Constant: ').grid(row=2, column=0)
        self.crossover_constant_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.crossover_constant_entry.insert(tk.END, '0.5')
        self.crossover_constant_entry.grid(row=2, column=1)

        # Population Size
        tk.Label(self.hyperparameters_frame, fg='black', text='Population Size: ').grid(row=3, column=0)
        self.pop_size_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.pop_size_entry.insert(tk.END, '100')
        self.pop_size_entry.grid(row=3, column=1)

        # Iteration Number
        tk.Label(self.hyperparameters_frame, fg='black', text='Iterations: ').grid(row=4, column=0)
        self.iter_num_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.iter_num_entry.insert(tk.END, '100')
        self.iter_num_entry.grid(row=4, column=1)

        # Selection function
        tk.Label(self.hyperparameters_frame, fg='black', text='Selection Function: ').grid(row=5, column=0)
        selection_options = [method for method in dir(Selection) if method.startswith('_') is False]
        selection_options = GUI.preprocessing_enums_for_option_menu(selection_options)
        self.selection_choice = tk.StringVar(self.hyperparameters_frame)
        self.selection_choice.set(selection_options[0])
        self.selection_menu = tk.OptionMenu(self.hyperparameters_frame, self.selection_choice, *selection_options)
        self.selection_menu.grid(row=5, column=1)

        # Mutation function
        tk.Label(self.hyperparameters_frame, fg='black', text='Mutation Function: ').grid(row=6, column=0)
        mutation_options = [method for method in dir(Mutation) if method.startswith('_') is False]
        mutation_options = GUI.preprocessing_enums_for_option_menu(mutation_options)
        self.mutation_choice = tk.StringVar(self.hyperparameters_frame)
        self.mutation_choice.set(mutation_options[0])
        self.mutation_menu = tk.OptionMenu(self.hyperparameters_frame, self.mutation_choice, *mutation_options)
        self.mutation_menu.grid(row=6, column=1)

        # Number of linear combinations
        tk.Label(self.hyperparameters_frame, fg='black', text='Number of Linear Combinations: ').grid(row=7, column=0)
        self.lin_comb_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.lin_comb_entry.insert(tk.END, '100')
        self.lin_comb_entry.grid(row=7, column=1)
        # endregion

    def run_algorithm(self, save=True):
        selection_fn = eval('Selection.' + GUI.preprocessing_option_menu_for_enum(self.selection_choice.get()))
        mutation_fn = eval('Mutation.' + GUI.preprocessing_option_menu_for_enum(self.mutation_choice.get()))
        crossover_fn = eval('Crossover.' + GUI.preprocessing_option_menu_for_enum(self.crossover_choice.get()))
        tsp_constraint_solver_fn = eval('TSPConstraintSolver.' + GUI.preprocessing_option_menu_for_enum(self.solver_choice.get()))

        pop_size = int(self.pop_size_entry.get())
        iter_num = int(self.iter_num_entry.get())
        crossover_constant = float(self.crossover_constant_entry.get())
        lin_comb_num = int(self.lin_comb_entry.get())

        de = DifferentialEvolution(selection_fn=selection_fn, mutation_fn=mutation_fn, crossover_fn=crossover_fn, tsp_constraint_solver_fn=tsp_constraint_solver_fn, pop_size=pop_size, iter_num=iter_num, crossover_constant=crossover_constant, lin_comb_num=lin_comb_num)
        solutions = de.solve(self.problem)

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
            'Algorithm type: ': 'Simple Immunological Algorithm',
            'Selection Function: ': self.selection_choice.get(),
            'Mutation Function': self.mutation_choice.get(),
            'Crossover Function': self.crossover_choice.get(),
            'TSP Constraint Solver: ': self.solver_choice.get(),
            'Population Size: ': self.pop_size_entry.get(),
            'Iteration Number: ': self.iter_num_entry.get(),
            'Crossover Constant: ': self.crossover_choice.get(),
            'Linear Combination Number: ': self.lin_comb_entry.get(),
            'Fit: ': fit

        }
        with open(f'{directory}/{new_name}.txt', 'w+') as f:
            for key, val in zip(list(vals.keys()), list(vals.values())):
                f.write(f'{key}={val}\n_')
        print("Results saved")
