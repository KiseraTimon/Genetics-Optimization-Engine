"""
Module: core.models.chromosome.py

Defines the biological data structures.
"""

from typing import List, Any

class Chromosome:
    """
    Represents an individual candidate solution in the population.
    Encapsulates both the genetic data (genes) and its evaluated fitness.
    """
    def __init__(self, genes: List[Any]):
        self.genes = genes
        self.fitness = 0.0

    def __repr__(self):
        """String representation for easier debugging and logging."""
        gene_str = "".join(str(g) for g in self.genes)
        return f"[{gene_str}] (Fitness: {self.fitness})"