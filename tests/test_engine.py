import pytest
from core.engine import EvolutionEngine
from core.environments.text_env import TextEnvironment
from core.operators.selection import TournamentSelection
from core.operators.crossover import CrossoverStrategy
from core.operators.mutation import MutationStrategy
from core.models.chromosome import Chromosome
import random

# Mock Crossover for Text (Since OX1 is for permutations)
class SinglePointCrossover(CrossoverStrategy):
    def crossover(self, p1, p2):
        pt = len(p1.genes) // 2
        return Chromosome(p1.genes[:pt] + p2.genes[pt:]), Chromosome(p2.genes[:pt] + p1.genes[pt:])

# Mock Mutation for Text
class PointMutation(MutationStrategy):
    def mutate(self, chromosome, mutation_rate, gene_pool=None):
        if random.random() < mutation_rate:
            chromosome.genes[0] = 'X' # Simple forced mutation for testing

@pytest.fixture
def engine():
    env = TextEnvironment("TEST")
    return EvolutionEngine(
        environment=env,
        selector=TournamentSelection(tournament_size=2),
        crossover_op=SinglePointCrossover(),
        mutator=PointMutation(),
        pop_size=10, # Very small population for fast tests
        base_mutation_rate=0.1
    )

def test_engine_initialization(engine):
    engine._initialize_population()
    assert len(engine.population) == 10

def test_fitness_evaluation_sorting(engine):
    engine._initialize_population()
    
    # Manually rig fitness to test sorting
    engine.population[0].fitness = 1.0
    engine.population[-1].fitness = 100.0
    
    engine._evaluate_fitness_parallel()
    
    # The highest fitness should now be at index 0
    assert engine.population[0].fitness >= engine.population[-1].fitness

def test_stagnation_tracking_and_mutation_adaptation(engine):
    # Simulate stagnation
    engine.last_best_fitness = 5.0
    engine._adapt_mutation_rate(current_best_fitness=5.0) # Matches last
    
    assert engine.stagnation_counter == 1
    
    # Force heavy stagnation
    engine.stagnation_counter = 20
    engine._adapt_mutation_rate(current_best_fitness=5.0)
    
    # Mutation should scale by 1.5
    assert engine.current_mutation_rate > engine.base_mutation_rate