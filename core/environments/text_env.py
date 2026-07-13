"""
Module: text_env.py
Implementation of the Synthetic Text Evolution sandbox.
"""

import random
import string
from typing import List
from core.environments.base import BaseEnvironment


class TextEnvironment(BaseEnvironment):
    def __init__(self, target_string: str = "HELLO WORLD"):
        """
        Initializes the text landscape.
        The target string defines the global optimum we are searching for.
        """

        self.target = target_string
        self.genome_length = len(target_string)
        # The gene pool: Uppercase letters + space
        self.gene_pool = string.ascii_uppercase + " "
        self._is_solved = False

    def generate_random_chromosome(self) -> List[str]:
        """Fills a new chromosome with random characters from the gene pool."""
        return [random.choice(self.gene_pool) for _ in range(self.genome_length)]

    def evaluate_fitness(self, chromosome: List[str]) -> float:
        """
        Compares the candidate chromosome against the target string index by index.
        A perfect match yields a score equal to the genome_length.
        """
        score = sum(1 for i, gene in enumerate(chromosome) if gene == self.target[i])
        
        # Flag if the global optimum is found
        if score == self.genome_length:
            self._is_solved = True
            
        return float(score)
        
    @property
    def is_solved(self) -> bool:
        return self._is_solved