import pytest
import random
from core.models.chromosome import Chromosome
from core.operators.selection import TournamentSelection, RouletteWheelSelection
from core.operators.crossover import OrderCrossover
from core.operators.mutation import SwapMutation

@pytest.fixture
def population():
    c1, c2, c3 = Chromosome([1, 2, 3]), Chromosome([4, 5, 6]), Chromosome([7, 8, 9])
    c1.fitness, c2.fitness, c3.fitness = 10.0, 50.0, 5.0
    return [c1, c2, c3]

def test_tournament_selection(population):
    # Tournament size equal to pop ensures the absolute best is always picked
    selector = TournamentSelection(tournament_size=3)
    winner = selector.select(population)
    assert winner.fitness == 50.0

def test_order_crossover():
    p1 = Chromosome([0, 1, 2, 3, 4, 5])
    p2 = Chromosome([5, 4, 3, 2, 1, 0])
    
    crossover = OrderCrossover()
    child1, child2 = crossover.crossover(p1, p2)
    
    # OX1 must preserve the exact length
    assert len(child1.genes) == 6
    assert len(child2.genes) == 6
    
    # OX1 must not create duplicates or lose genes (must remain a permutation)
    assert set(child1.genes) == set(p1.genes)
    assert set(child2.genes) == set(p2.genes)

def test_swap_mutation():
    original_genes = [0, 1, 2, 3, 4]
    chrom = Chromosome(original_genes.copy())
    
    mutator = SwapMutation()
    
    # Force mutation by setting rate to 1.0 (100% chance)
    random.seed(42) # Lock seed for deterministic behavior
    mutator.mutate(chrom, mutation_rate=1.0)
    
    # Ensure genes changed but elements remain the same
    assert chrom.genes != original_genes
    assert set(chrom.genes) == set(original_genes)