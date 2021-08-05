import tkinter as tk
import os
from AlgorithmGUI import AlgorithmGUI
from ASA.AntSystemAlgorithm import AntSystemAlgorithm
from ASA.Operators.LocalSearch import LocalSearch
from ASA.Operators.PheromoneDeposition import PheromoneDeposition

class GUI(AlgorithmGUI):
    def __init__(self, problem, master_frame, filename, position=(0,0)):
        self.master_frame = master_frame
        self.problem = problem
        self.filename = filename

        # region Hyperparameters
        self.hyperparameters_frame = tk.LabelFrame(self.master_frame, text='HYPERPARAMETERS', padx=5, pady=5)
        self.hyperparameters_frame.grid(row=position[0], column=position[1], columnspan=2)

        # Local Search Algorithm
        tk.Label(self.hyperparameters_frame, fg='black', text='Initial Local Search Algorithm: ').grid(row=0, column=0)
        local_search_options = [method for method in dir(LocalSearch) if method.startswith('_') is False]
        local_search_options = GUI.preprocessing_enums_for_option_menu(local_search_options)
        self.local_search_choice = tk.StringVar(self.hyperparameters_frame)
        self.local_search_choice.set(local_search_options[0])
        self.local_search_menu = tk.OptionMenu(self.hyperparameters_frame, self.local_search_choice, *local_search_options)
        self.local_search_menu.grid(row=0, column=1)

        # Pheromone deposition function
        tk.Label(self.hyperparameters_frame, fg='black', text='Pheromone Deposition Function: ').grid(row=1, column=0)
        pheromone_deposition_options = [method for method in dir(PheromoneDeposition) if method.startswith('_') is False]
        pheromone_deposition_options = GUI.preprocessing_enums_for_option_menu(pheromone_deposition_options)
        self.pheromone_deposition_choice = tk.StringVar(self.hyperparameters_frame)
        self.pheromone_deposition_choice.set(pheromone_deposition_options[0])
        self.pheromone_deposition_menu = tk.OptionMenu(self.hyperparameters_frame, self.pheromone_deposition_choice, *pheromone_deposition_options)
        self.pheromone_deposition_menu.grid(row=1, column=1)

        # Alpha constant
        tk.Label(self.hyperparameters_frame, fg='black', text='Alpha Constant: ').grid(row=2, column=0)
        self.alpha_constant_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.alpha_constant_entry.insert(tk.END, '1.')
        self.alpha_constant_entry.grid(row=2, column=1)

        # Beta constant
        tk.Label(self.hyperparameters_frame, fg='black', text='Beta Constant: ').grid(row=3, column=0)
        self.beta_constant_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.beta_constant_entry.insert(tk.END, '2.5')
        self.beta_constant_entry.grid(row=3, column=1)

        # Phi constant
        tk.Label(self.hyperparameters_frame, fg='black', text='Pheromone Evaporation Coefficient: ').grid(row=4, column=0)
        self.phi_constant_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.phi_constant_entry.insert(tk.END, '0.5')
        self.phi_constant_entry.grid(row=4, column=1)

        # Population Size
        tk.Label(self.hyperparameters_frame, fg='black', text='Population Size: ').grid(row=5, column=0)
        self.pop_size_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.pop_size_entry.insert(tk.END, '100')
        self.pop_size_entry.grid(row=5, column=1)

        # Iteration Number
        tk.Label(self.hyperparameters_frame, fg='black', text='Iterations: ').grid(row=6, column=0)
        self.iter_num_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.iter_num_entry.insert(tk.END, '100')
        self.iter_num_entry.grid(row=6, column=1)
        # endregion

    def run_algorithm(self, save=True):
        pheromone_deposition_fn = eval('PheromoneDeposition.' + GUI.preprocessing_option_menu_for_enum(self.pheromone_deposition_choice.get()))
        local_search_fn = eval('LocalSearch.' + GUI.preprocessing_option_menu_for_enum(self.local_search_choice.get()))

        pop_size = int(self.pop_size_entry.get())
        iter_num = int(self.iter_num_entry.get())
        alpha = float(self.alpha_constant_entry.get())
        beta = float(self.beta_constant_entry.get())
        phi = float(self.phi_constant_entry.get())

        de = AntSystemAlgorithm(alpha=alpha, beta=beta, phi=phi, iter_num=iter_num, pop_size=pop_size, local_search_fn=local_search_fn, pheromone_deposition_fn=pheromone_deposition_fn)
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
            'Local Search Function: ': self.local_search_choice.get(),
            'Pheromone Deposition Function: ': self.pheromone_deposition_choice.get(),
            'Alpha Constant: ': self.alpha_constant_entry.get(),
            'Beta Constant: ': self.beta_constant_entry.get(),
            'Pheromone Evaporation Coefficient: ': self.phi_constant_entry.get(),
            'Iteration Number: ': self.iter_num_entry.get(),
            'Population Size: ': self.pop_size_entry.get(),
            'Fit: ': fit
        }
        with open(f'{directory}/{new_name}.txt', 'w+') as f:
            for key, val in zip(list(vals.keys()), list(vals.values())):
                f.write(f'{key}={val}\n_')
        print("Results saved")
