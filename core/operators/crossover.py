"""
Module: core.operators.crossover.py

Implements the Strategy Pattern for crossovers
"""

from typing import Tuple
from core.models.chromosome import Chromosome

class CrossoverStrategy:
    def crossover(self, p1: Chromosome, p2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        raise NotImplementedError