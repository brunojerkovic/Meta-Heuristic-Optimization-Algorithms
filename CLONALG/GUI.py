import tkinter as tk
import os
from CLONALG.ClonAlg import ClonAlg
from AlgorithmGUI import AlgorithmGUI
from CLONALG.Operators.Hypermutation import Hypermutation
from CLONALG.Operators.Cloning import Cloning

class GUI(AlgorithmGUI):
    def __init__(self, problem, master_frame, filename, position=(0,0)):
        self.master_frame = master_frame
        self.problem = problem
        self.filename = filename

        # region Hyperparameters
        self.hyperparameters_frame = tk.LabelFrame(self.master_frame, text='HYPERPARAMETERS', padx=5, pady=5)
        self.hyperparameters_frame.grid(row=position[0], column=position[1], columnspan=2)

        # Hypermutation
        tk.Label(self.hyperparameters_frame, fg='black', text='Hypermutation Function: ').grid(row=0, column=0)
        hypermutation_options = [method for method in dir(Hypermutation) if method.startswith('_') is False]
        hypermutation_options = GUI.preprocessing_enums_for_option_menu(hypermutation_options)
        self.hypermutation_choice = tk.StringVar(self.hyperparameters_frame)
        self.hypermutation_choice.set(hypermutation_options[0])
        self.hypermutation_menu = tk.OptionMenu(self.hyperparameters_frame, self.hypermutation_choice, *hypermutation_options)
        self.hypermutation_menu.grid(row=0, column=1)

        # Hypermutation Constant
        tk.Label(self.hyperparameters_frame, fg='black', text='Hypermutation Constant: ').grid(row=1, column=0)
        self.hypermutation_constant_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.hypermutation_constant_entry.insert(tk.END, '2.0')
        self.hypermutation_constant_entry.grid(row=1, column=1)

        # Population Size
        tk.Label(self.hyperparameters_frame, fg='black', text='Population Size: ').grid(row=2, column=0)
        self.pop_size_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.pop_size_entry.insert(tk.END, '100')
        self.pop_size_entry.grid(row=2, column=1)

        # Iteration Number
        tk.Label(self.hyperparameters_frame, fg='black', text='Iterations: ').grid(row=3, column=0)
        self.iter_num_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.iter_num_entry.insert(tk.END, '100')
        self.iter_num_entry.grid(row=3, column=1)

        # Cloning Function
        tk.Label(self.hyperparameters_frame, fg='black', text='Hypermutation Function: ').grid(row=4, column=0)
        cloning_options = [method for method in dir(Cloning) if method.startswith('_') is False]
        cloning_options = GUI.preprocessing_enums_for_option_menu(cloning_options)
        self.cloning_choice = tk.StringVar(self.hyperparameters_frame)
        self.cloning_choice.set(cloning_options[0])
        self.cloning_menu = tk.OptionMenu(self.hyperparameters_frame, self.cloning_choice, *cloning_options)
        self.cloning_menu.grid(row=4, column=1)

        # Number of duplications of each solution
        tk.Label(self.hyperparameters_frame, fg='black', text='Duplication Number: ').grid(row=5, column=0)
        self.dup_num_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.dup_num_entry.insert(tk.END, '3')
        self.dup_num_entry.grid(row=5, column=1)
        # endregion

    def run_algorithm(self, save=True):
        hypermutation_fn = eval('Hypermutation.' + GUI.preprocessing_option_menu_for_enum(self.hypermutation_choice.get()))
        hypermutation_constant = float(self.hypermutation_constant_entry.get())
        pop_size = int(self.pop_size_entry.get())
        iter_num = int(self.iter_num_entry.get())
        cloning_fn = eval('Cloning.' + GUI.preprocessing_option_menu_for_enum(self.cloning_choice.get()))
        dup_num = int(self.dup_num_entry.get())

        clonalg = ClonAlg(cloning_fn=cloning_fn, hypermutation_fn=hypermutation_fn, hypermutation_constant=hypermutation_constant, pop_size=pop_size, iter_num=iter_num, dup_num=dup_num)
        solutions = clonalg.solve(self.problem)

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
            'Algorithm Type: ': 'Simple Immunological Algorithm',
            'Hypermutation: ': self.hypermutation_choice.get(),
            'Hypermutation Constant': self.hypermutation_constant_entry.get(),
            'Population Size': self.pop_size_entry.get(),
            'Iteration Number: ': self.iter_num_entry.get(),
            'Cloning Function: ': self.cloning_choice.get(),
            'Duplication Size: ': self.dup_num_entry.get(),
            'Fit: ': fit

        }
        with open(f'{directory}/{new_name}.txt', 'w+') as f:
            for key, val in zip(list(vals.keys()), list(vals.values())):
                f.write(f'{key}={val}\n_')
        print("Results saved")
