"""
Module: environments/tsp_env.py
Empirical spatial optimization environment.
"""

import random
import math
from typing import List, Tuple
from core.environments.base import BaseEnvironment

class TSPEnvironment(BaseEnvironment):
    """
    Evaluates fitness based on Euclidean distance between continuous coordinate points.
    """

    def __init__(self, num_cities: int = 50, grid_size: int = 1000):
        self.num_cities = num_cities
        self.grid_size = grid_size

        # Generate synthetic coordinate data mimicking empirical spatial datasets
        self.cities: List[Tuple[int, int]] = [
            (random.randint(0, grid_size), random.randint(0, grid_size)) 
            for _ in range(num_cities)
        ]

        # Pre-compute distance matrix for mathematical precision and speed O(1) lookups
        self.distance_matrix = self._build_distance_matrix()
        self._is_solved = False

    def _build_distance_matrix(self) -> List[List[float]]:
        matrix = [[0.0] * self.num_cities for _ in range(self.num_cities)]
        for i in range(self.num_cities):
            for j in range(self.num_cities):
                if i != j:
                    x1, y1 = self.cities[i]
                    x2, y2 = self.cities[j]
                    matrix[i][j] = math.hypot(x1 - x2, y1 - y2)
        return matrix

    def generate_random_chromosome(self) -> List[int]:
        """A valid chromosome is a complete permutation of all city indices."""
        route = list(range(self.num_cities))
        random.shuffle(route)
        return route

    def evaluate_fitness(self, chromosome: List[int]) -> float:
        """
        Objective Function: Minimization of path length.
        Returns the inverse of total distance so the GA can maximize it.
        """
        total_distance = 0.0
        for i in range(self.num_cities):
            from_city = chromosome[i]

            # Wrap around to the start city to complete the loop
            to_city = chromosome[(i + 1) % self.num_cities] 
            total_distance += self.distance_matrix[from_city][to_city]
        
        # Fitness is inverted distance
        return 1.0 / total_distance if total_distance > 0 else 0

    @property
    def is_solved(self) -> bool:
        # TSP has no known distinct global optimum stopping point without exhaustive search
        return False