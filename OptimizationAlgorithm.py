import abc

# Base class for the specific algorithm
class OptimizationAlgorithm(metaclass=abc.ABCMeta):
   @abc.abstractmethod
   def solve(self, problem):
      pass
