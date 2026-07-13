"""
Module: core/engine.py
Advanced Evolutionary Loop managing parallel evaluation, dynamic hyperparameters, 
and strategy execution.
"""
from concurrent.futures import ThreadPoolExecutor
from typing import List

from core.models.chromosome import Chromosome
from core.environments.base import BaseEnvironment
from core.operators.selection import SelectionStrategy
from core.operators.crossover import CrossoverStrategy
from core.operators.mutation import MutationStrategy
from utils.metrics import TelemetryTracker

class EvolutionEngine:
    def __init__(
        self,
        environment: BaseEnvironment,
        selector: SelectionStrategy,
        crossover_op: CrossoverStrategy,
        mutator: MutationStrategy,
    ):
        # Injected Dependencies
        self.env = environment
        self.selector = selector
        self.crossover_op = crossover_op
        self.mutator = mutator
        
        # System State
        self.population: List[Chromosome] = []
        self.telemetry = TelemetryTracker()
        self.stagnation_counter = 0
        self.last_best_fitness = 0.0