import numpy as np
import tkinter as tk
import time
import settings

class TestingGUI:
    def __init__(self):
        self.set_gui()

    def set_gui(self):
        # Set window
        self.master_frame = tk.Tk()
        self.master_frame.title("Natural Computing Algorithms Testing Interface")

        # region Main Menu
        self.main_menu_frame = tk.LabelFrame(self.master_frame, text='MAIN MENU', padx=5, pady=5)
        self.main_menu_frame.grid(row=0, column=0)

        tk.Label(self.main_menu_frame, fg='black', text='Algorithm: ').grid(row=0, column=0)
        algorithm_options = settings.algorithms
        algorithm_options.sort()
        self.algorithm_choice = tk.StringVar(self.main_menu_frame)
        self.algorithm_choice.set(algorithm_options[0])
        self.sel_tt_menu = tk.OptionMenu(self.main_menu_frame, self.algorithm_choice, *algorithm_options)
        self.sel_tt_menu.grid(row=0, column=1)
        # endregion

        # region Main Menu
        self.main_menu_frame = tk.LabelFrame(self.master_frame, text='MAIN MENU', padx=5, pady=5)
        self.main_menu_frame.grid(row=0, column=0)

        tk.Label(self.main_menu_frame, fg='black', text='Algorithm: ').grid(row=0, column=0)
        algorithm_options = settings.algorithms
        algorithm_options.sort()
        self.algorithm_choice = tk.StringVar(self.main_menu_frame)
        self.algorithm_choice.set(algorithm_options[0])
        self.sel_tt_menu = tk.OptionMenu(self.main_menu_frame, self.algorithm_choice, *algorithm_options)
        self.sel_tt_menu.grid(row=0, column=1)
        # endregion

    def run(self):
        self.master_frame.mainloop()

def open_gui():
    window = TestingGUI()
    window.run()