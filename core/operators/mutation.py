"""
Module: core.operators.mutations.py

Implements the Strategy Pattern for mutation
"""

from typing import List
from core.models.chromosome import Chromosome

class MutationStrategy:
    def mutate(self, chromosome: Chromosome, mutation_rate: float, gene_pool: List = []):
        raise NotImplementedError