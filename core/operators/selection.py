"""
Module: core.operators.selection.py

Implements the Strategy Pattern for selection
"""

from typing import List
from core.models.chromosome import Chromosome

# base
class SelectionStrategy:
    """Base class for selection mechanics."""
    def select(self, population: List[Chromosome], **kwargs) -> Chromosome:
        raise NotImplementedError