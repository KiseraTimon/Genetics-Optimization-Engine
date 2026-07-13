"""
Module: core.operators.crossover.py

Implements the Strategy Pattern for crossovers
"""

import random
from typing import Tuple
from core.models.chromosome import Chromosome

class CrossoverStrategy:
    def crossover(self, p1: Chromosome, p2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        raise NotImplementedError

class OrderCrossover(CrossoverStrategy):
    """
    Order Crossover (OX1).
    Strictly required for combinatorial problems like TSP to prevent duplicate/missing genes.
    """
    def crossover(self, p1: Chromosome, p2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        size = len(p1.genes)
        start, end = sorted(random.sample(range(size), 2))
        
        def ox1(parentA, parentB):
            child = [None] * size

            # Copy genetic swath from Parent A
            child[start:end] = parentA.genes[start:end]

            # Fill remaining with genes from Parent B, preserving order
            b_idx = 0
            for i in range(size):
                if child[i] is None:
                    while parentB.genes[b_idx] in child:
                        b_idx += 1
                    child[i] = parentB.genes[b_idx]
            return Chromosome(child)

        return ox1(p1, p2), ox1(p2, p1)