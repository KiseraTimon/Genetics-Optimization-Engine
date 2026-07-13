"""
main.py
Execution Entry Point.
Wires the TSP environment to the evolutionary engine and begins optimization.
"""
from core.environments.tsp_env import TSPEnvironment
from core.engine import EvolutionEngine
from core.operators.selection import TournamentSelection
from core.operators.crossover import OrderCrossover
from core.operators.mutation import SwapMutation


def main():
    print("Initializing Engineered GA Framework: TSP Module")
    print("=" * 60)
    
    # 1. Initialize Spatial Environment (50 cities)
    env = TSPEnvironment(num_cities=50, grid_size=1000)
    
    # 2. Inject Strategy Patterns strictly designed for path optimization
    selector = TournamentSelection(tournament_size=5)
    crossover = OrderCrossover()
    mutator = SwapMutation()
    
    # 3. Build and Run Engine
    engine = EvolutionEngine(
        environment=env,
        selector=selector,
        crossover_op=crossover,
        mutator=mutator,
        pop_size=300,
        base_mutation_rate=0.08
    )
    
    print("Engine configured. Commencing generational evolution...")
    best_route = engine.run(max_generations=1000)
    
    print("=" * 60)
    print("Optimization Complete.")
    print(f"Final Optimal Route Fitness: {best_route.fitness:05.6f}")
    
    # Convert fitness back to human-readable distance (1 / fitness)
    distance = 1.0 / best_route.fitness if best_route.fitness > 0 else float('inf')
    print(f"Total Distance Traveled:     {distance:.2f} units")


if __name__ == "__main__":
    main()