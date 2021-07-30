import abc


class OptimizationAlgorithm(metaclass=abc.ABCMeta):
   @abc.abstractmethod
   def solve(self):
      pass
