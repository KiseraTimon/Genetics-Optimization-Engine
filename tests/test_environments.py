import pytest
from core.environments.text_env import TextEnvironment
from core.environments.tsp_env import TSPEnvironment

class TestTextEnvironment:
    @pytest.fixture
    def env(self):
        return TextEnvironment(target_string="TEST")

    def test_initialization(self, env):
        assert env.genome_length == 4
        assert not env.is_solved

    def test_random_chromosome_generation(self, env):
        chrom = env.generate_random_chromosome()
        assert len(chrom) == 4
        assert all(isinstance(g, str) for g in chrom)

    def test_evaluate_fitness(self, env):
        # Perfect match
        assert env.evaluate_fitness(['T', 'E', 'S', 'T']) == 4.0
        assert env.is_solved is True

        # Partial match
        assert env.evaluate_fitness(['T', 'E', 'X', 'X']) == 2.0

class TestTSPEnvironment:
    @pytest.fixture
    def env(self):
        # Small environment for testing
        return TSPEnvironment(num_cities=5, grid_size=100)

    def test_distance_matrix_dimensions(self, env):
        assert len(env.distance_matrix) == 5
        assert len(env.distance_matrix[0]) == 5

    def test_random_chromosome_is_permutation(self, env):
        chrom = env.generate_random_chromosome()
        assert len(chrom) == 5
        assert set(chrom) == {0, 1, 2, 3, 4} # Must contain exact unique indices

    def test_fitness_is_inverted_distance(self, env):
        chrom = [0, 1, 2, 3, 4]
        fitness = env.evaluate_fitness(chrom)
        assert fitness > 0
        assert isinstance(fitness, float)