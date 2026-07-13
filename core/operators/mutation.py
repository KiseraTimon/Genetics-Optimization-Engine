"""
Module: core.operators.mutations.py

Implements the Strategy Pattern for mutation
"""

import random
from typing import List
from core.models.chromosome import Chromosome

class MutationStrategy:
    def mutate(self, chromosome: Chromosome, mutation_rate: float, gene_pool: List = []):
        raise NotImplementedError


class SwapMutation(MutationStrategy):
    """
    Randomly swaps the position of two genes.
    Highly effective for pathing problems (TSP).
    """
    def mutate(self, chromosome: Chromosome, mutation_rate: float, gene_pool: List = []):
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(chromosome.genes)), 2)
            chromosome.genes[idx1], chromosome.genes[idx2] = chromosome.genes[idx2], chromosome.genes[idx1]