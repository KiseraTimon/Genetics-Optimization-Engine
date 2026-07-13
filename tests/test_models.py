import pytest
from core.models.chromosome import Chromosome

def test_chromosome_initialization():
    genes = [1, 2, 3, 4]
    chrom = Chromosome(genes)
    
    assert chrom.genes == genes
    assert chrom.fitness == 0.0

def test_chromosome_repr():
    chrom = Chromosome(['A', 'B', 'C'])
    chrom.fitness = 5.5
    
    rep = repr(chrom)
    assert "[ABC]" in rep
    assert "5.5" in rep