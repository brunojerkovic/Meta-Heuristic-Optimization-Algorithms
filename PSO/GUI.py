import tkinter as tk
import os
from PSO.ParticleSwarmOptimization import ParticleSwarmOptimization
from AlgorithmGUI import AlgorithmGUI
from PSO.Operators.VelocityUpdate import VelocityUpdate

class GUI(AlgorithmGUI):
    def __init__(self, problem, master_frame, filename, position=(0,0)):
        self.master_frame = master_frame
        self.problem = problem
        self.filename = filename

        # region Hyperparameters
        self.hyperparameters_frame = tk.LabelFrame(self.master_frame, text='HYPERPARAMETERS', padx=5, pady=5)
        self.hyperparameters_frame.grid(row=position[0], column=position[1], columnspan=2)

        # Minimum Velocity
        tk.Label(self.hyperparameters_frame, fg='black', text='Minimum Velocity: ').grid(row=0, column=0)
        self.min_vel_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.min_vel_entry.insert(tk.END, '1')
        self.min_vel_entry.grid(row=0, column=1)

        # Maximum Velocity
        tk.Label(self.hyperparameters_frame, fg='black', text='Maximum Velocity: ').grid(row=1, column=0)
        self.max_vel_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.max_vel_entry.insert(tk.END, '30')
        self.max_vel_entry.grid(row=1, column=1)

        # Population size
        tk.Label(self.hyperparameters_frame, fg='black', text='Population Size: ').grid(row=2, column=0)
        self.pop_size_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.pop_size_entry.insert(tk.END, '100')
        self.pop_size_entry.grid(row=2, column=1)

        # Iteration Number
        tk.Label(self.hyperparameters_frame, fg='black', text='Iterations per temperature value: ').grid(row=3, column=0)
        self.iter_num_entry = tk.Entry(self.hyperparameters_frame, fg='black', bg='white', width=10)
        self.iter_num_entry.insert(tk.END, '100')
        self.iter_num_entry.grid(row=3, column=1)

        # Velocity Update
        tk.Label(self.hyperparameters_frame, fg='black', text='Cooling Plan: ').grid(row=4, column=0)
        velocity_update_options = [method for method in dir(VelocityUpdate) if method.startswith('_') is False]
        velocity_update_options = GUI.preprocessing_enums_for_option_menu(velocity_update_options)
        self.velocity_update_choice = tk.StringVar(self.hyperparameters_frame)
        self.velocity_update_choice.set(velocity_update_options[0])
        self.velocity_update_menu = tk.OptionMenu(self.hyperparameters_frame, self.velocity_update_choice, *velocity_update_options)
        self.velocity_update_menu.grid(row=4, column=1)
        # endregion

    def run_algorithm(self, save=True):
        pop_size = int(self.pop_size_entry.get())
        min_vel = int(self.pop_size_entry.get())
        max_vel = int(self.pop_size_entry.get())
        iter_num = int(self.iter_num_entry.get())
        velocity_update_fn = eval('VelocityUpdate.' + GUI.preprocessing_option_menu_for_enum(self.velocity_update_choice.get()))

        pso = ParticleSwarmOptimization(pop_size=pop_size, min_vel=min_vel, max_vel=max_vel, iter_num=iter_num, velocity_update_fn=velocity_update_fn)
        solutions = pso.solve(self.problem)

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
            'Algorithm type: ': 'Particle Swarm Optimization',
            'Population size: ': str(self.pop_size_entry.get()),
            'Max velocity: ': str(self.max_vel_entry.get()),
            'Min velocity: ': str(self.min_vel_entry.get()),
            'Iteration number: ': self.iter_num_entry.get(),
            'Fit: ': fit
        }
        with open(f'{directory}/{new_name}.txt', 'w+') as f:
            for key, val in zip(list(vals.keys()), list(vals.values())):
                f.write(f'{key}={val}\n_')
        print("Results saved")
