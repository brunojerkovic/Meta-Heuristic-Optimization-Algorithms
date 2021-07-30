import tkinter as tk
from tkinter import ttk
import time
import settings
from Problem.ProblemTSP import ProblemTSP

class TestingGUI:
    def __init__(self):
        self.time_passed = 0.
        self.score = 0.
        self.optimization_algorithm = None
        self.set_gui()

    def set_gui(self):
        # Set window
        self.master_frame = tk.Tk()
        self.master_frame.title("Natural Computing Algorithms Testing Interface")

        # region Main Menu
        self.main_menu_frame = tk.LabelFrame(self.master_frame, text='MAIN MENU', padx=5, pady=5)
        self.main_menu_frame.grid(row=0, column=0)

        # Algorithm type
        tk.Label(self.main_menu_frame, fg='black', text='Algorithm: ').grid(row=0, column=0)
        algorithm_options = settings.algorithms
        algorithm_options.sort()
        self.algorithm_choice = tk.StringVar(self.main_menu_frame)
        self.algorithm_choice.set(algorithm_options[0])
        self.algorithm_type_menu = tk.OptionMenu(self.main_menu_frame, self.algorithm_choice, *algorithm_options)
        self.algorithm_type_menu.grid(row=0, column=1)

        # Dataset path
        tk.Label(self.main_menu_frame, fg='black', text='Dataset Path: ').grid(row=1, column=0)
        self.dataset_path_entry = tk.Entry(self.main_menu_frame, fg='black', bg='white', width=50)
        self.dataset_path_entry.insert(tk.END, 'Datasets/dj38.tsp')
        self.dataset_path_entry.grid(row=1, column=1)

        # Start button
        self.start_button = tk.Button(self.main_menu_frame, text='START', cursor='hand2')
        self.start_button.bind('<Button-1>', self.start_button_clicked)
        self.start_button.grid(row=2, column=0, columnspan=2)

        # Progressbar
        self.progressbar = ttk.Progressbar(self.main_menu_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progressbar.grid(row=3, column=0, columnspan=2)

        # Time passed
        self.time_str = tk.StringVar(self.main_menu_frame)
        self.time_str.set(f'Time: {round(self.time_passed, 2)}')
        self.time_label = tk.Label(self.main_menu_frame, fg='black', textvariable=self.time_str)
        self.time_label.grid(row=4, column=0, columnspan=2)

        # Score
        self.score_str = tk.StringVar(self.main_menu_frame)
        self.score_str.set(f'Time: {round(self.score, 2)}')
        self.score_label = tk.Label(self.main_menu_frame, fg='black', textvariable=self.score_str)
        self.score_label.grid(row=5, column=0, columnspan=2)

        # ALgorithm GUI
        AlgorithmGUI = self.get_algorithm_gui()
        if AlgorithmGUI is not None:
            self.gui = AlgorithmGUI(self.master_frame, position=(0, 2))
        # endregion

    def start_button_clicked(self):
        # Start timer and restart progress bar
        self.time_passed = 0.
        start_time = time.time()
        self.progressbar['value'] = 0.

        # Load the problem
        filename = self.dataset_path_entry.get().replace("\\", "/")
        self.problem = ProblemTSP()
        self.problem.read_file(filename)

        # Init GUI


        # Find the best solution with GA
        best_solution, avg_fits = myGA.run(iter_num)

        # End timer
        self.time_passed = time.time() - self.start_time

        # Save the results
        if self.save_img_choice.get() == 1:
            myGA.save_results(best_solution, avg_fits, filename)

    def get_algorithm_gui(self):
        algorithm_str = self.algorithm_choice.get()

        if algorithm_str == 'Simulated Annealing':
            from SA.GUI import GUI # TODO: samo importaj odredjeni GUI
        else:
            GUI = None

        return GUI

    def run(self):
        self.master_frame.mainloop()

def open_gui():
    window = TestingGUI()
    window.run()