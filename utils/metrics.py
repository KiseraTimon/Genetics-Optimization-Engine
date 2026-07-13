"""
Module: utils.metrics.py

Handles telemetry, performance tracking, and data export for the evolutionary engine.
This decouples data logging from the core mathematical loop.
"""

import csv
from pathlib import Path
from typing import List, Dict, Any

class TelemetryTracker:
    """
    Tracks the performance metrics of the Genetic Algorithm across generations.
    Stores data in memory during execution and provides methods for disk export.
    """
    def __init__(self):
        # In-memory storage for the run's historical data
        self.history: List[Dict[str, Any]] = []

    def log(self, generation: int, best_fitness: float, mutation_rate: float) -> None:
        """
        Records the statistics for a single generation.

        Args:
            generation (int): The current epoch/generation number.
            best_fitness (float): The highest fitness score achieved in this generation.
            mutation_rate (float): The current mutation rate (useful for tracking dynamic scaling).
        """

        # Append the current state to our history tracker
        self.history.append({
            "generation": generation,
            "best_fitness": best_fitness,
            "mutation_rate": mutation_rate
        })

        # Output a clean console log for real-time monitoring
        print(
            f"Gen {generation:04d} | "
            f"Max Fitness: {best_fitness:09.4f} | "
            f"Active Mutation Rate: {mutation_rate:.3f}"
        )

    def export_to_csv(self, filename: str = "evolution_telemetry.csv") -> None:
        """
        Exports the tracked in-memory telemetry data to a comma-separated values file.
        This allows for post-run analysis and graphing of the fitness landscape.
        
        Args:
            filename (str): The destination file path.
        """
        if not self.history:
            print("[!] Warning: No telemetry data to export.")
            return

        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = self.history[0].keys()

        try:
            with filepath.open(mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                writer.writeheader()
                for row in self.history:
                    writer.writerow(row)

            print(f"\n[+] Telemetry successfully exported to: {filepath.resolve()}")
            
        except IOError as e:
            print(f"\n[!] Failed to write telemetry data to {filepath.name}. Error: {e}")