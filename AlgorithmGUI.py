import abc

# Base class for the GUI of the specific algorithm
class AlgorithmGUI(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run_algorithm(self):
        pass

    @staticmethod
    def preprocessing_enums_for_option_menu(vals: list):
        new_vals = []
        for val in vals:
            val_ = val.lower().replace('_', ' ')
            val_ = val_[0].upper() + val_[1:]
            new_vals.append(val_)
        return new_vals

    @staticmethod
    def preprocessing_option_menu_for_enum(val):
        return val.lower().replace(' ', '_')