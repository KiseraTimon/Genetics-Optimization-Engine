"""
Module: core.environments.base.py

Defines the abstract base class for all optimization environments.
This enforces a strict contract: any environment passed to the GA engine
MUST implement initialization and fitness evaluation methods.
"""

from abc import ABC, abstractmethod
from typing import List, Any

class BaseEnvironment(ABC):
    
    @abstractmethod
    def generate_random_chromosome(self) -> List[Any]:
        """
        Generates a randomized sequence of genes (the chromosome)
        valid within the specific search space.
        """
        pass

    @abstractmethod
    def evaluate_fitness(self, chromosome: List[Any]) -> float:
        """
        The Objective Function.
        Calculates a scalar value representing the performance of a chromosome.
        Higher values dictate higher fitness (maximization problem).
        """
        pass
        
    @property
    @abstractmethod
    def is_solved(self) -> bool:
        """Returns True if the global optimum has been reached."""
        pass