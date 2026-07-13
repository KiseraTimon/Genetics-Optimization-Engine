"""
Module: core.engine.py

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
        pop_size: int = 200,
        base_mutation_rate: float = 0.05
    ):
        # Injected Dependencies
        self.env = environment
        self.selector = selector
        self.crossover_op = crossover_op
        self.mutator = mutator
        
        # Hyperparameters
        self.pop_size = pop_size
        self.base_mutation_rate = base_mutation_rate
        self.current_mutation_rate = base_mutation_rate
        
        # System State
        self.population: List[Chromosome] = []
        self.telemetry = TelemetryTracker()
        self.stagnation_counter = 0
        self.last_best_fitness = 0.0

    def _initialize_population(self):
        """Phase 1: Seed the initial random population based on environment rules."""
        self.population = [
            Chromosome(self.env.generate_random_chromosome())
            for _ in range(self.pop_size)
        ]
        
    def _evaluate_fitness_parallel(self):
        """Phase 2: Evaluate fitness synchronously to avoid Python GIL overhead."""
        # fix: Removed ThreadPoolExecutor. Standard iteration is significantly faster here.
        fitnesses = [self.env.evaluate_fitness(ind.genes) for ind in self.population]
            
        for ind, fit in zip(self.population, fitnesses):
            ind.fitness = fit
            
        # Sort descending so population[0] is always the best
        self.population.sort(key=lambda x: x.fitness, reverse=True)

    def _adapt_mutation_rate(self, current_best_fitness: float):
        """Dynamic Hyperparameter Scaling to prevent premature convergence."""
        if current_best_fitness == self.last_best_fitness:
            self.stagnation_counter += 1
        else:
            self.stagnation_counter = 0
            self.last_best_fitness = current_best_fitness
            self.current_mutation_rate = self.base_mutation_rate

        # Induce a mutation shock if stagnant for 20 generations
        if self.stagnation_counter > 20:
            self.current_mutation_rate = min(0.5, self.current_mutation_rate * 1.5)

    def run(self, max_generations: int = 500) -> Chromosome:
        """Executes the discrete-time generational loop."""
        self._initialize_population()

        try:
            for gen in range(max_generations):
                self._evaluate_fitness_parallel()
                best_ind = self.population[0]
                
                self._adapt_mutation_rate(best_ind.fitness)
                self.telemetry.log(gen, best_ind.fitness, self.current_mutation_rate)

                # Check if environment dictates the problem is solved
                if self.env.is_solved:
                    print(f"\n[!] Global optimum achieved at Generation {gen}.")
                    break

                # Build Next Generation (Phase 3, 4, 5)
                elite_clone = Chromosome(best_ind.genes.copy())
                elite_clone.fitness = best_ind.fitness
                next_generation = [elite_clone] # Elitism
                
                while len(next_generation) < self.pop_size:
                    # Selection
                    p1 = self.selector.select(self.population)
                    p2 = self.selector.select(self.population)
                    
                    # Crossover
                    c1, c2 = self.crossover_op.crossover(p1, p2)
                    
                    # Mutation
                    self.mutator.mutate(c1, self.current_mutation_rate)
                    self.mutator.mutate(c2, self.current_mutation_rate)
                    
                    next_generation.extend([c1, c2])

                self.population = next_generation[:self.pop_size]
                
        finally:
            # Post-run cleanup and export
            self.telemetry.export_to_csv("evolution_telemetry.csv")

        return self.population[0]