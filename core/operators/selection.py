"""
Module: core.operators.selection.py

Implements the Strategy Pattern for selection
"""

import random
from typing import List
from core.models.chromosome import Chromosome

# base
class SelectionStrategy:
    """Base class for selection mechanics."""
    def select(self, population: List[Chromosome], **kwargs) -> Chromosome:
        raise NotImplementedError


class TournamentSelection(SelectionStrategy):
    """
    Selects the best individual from a random subset.
    High tournament sizes increase selection pressure.
    """
    def __init__(self, tournament_size: int = 5):
        self.tournament_size = tournament_size

    def select(self, population: List[Chromosome], **kwargs) -> Chromosome:
        tournament = random.sample(population, self.tournament_size)
        return max(tournament, key=lambda ind: ind.fitness)