import pytest
from utils.metrics import TelemetryTracker

def test_telemetry_logging():
    tracker = TelemetryTracker()
    tracker.log(generation=1, best_fitness=10.5, mutation_rate=0.05)
    
    assert len(tracker.history) == 1
    assert tracker.history[0]["generation"] == 1
    assert tracker.history[0]["best_fitness"] == 10.5

def test_telemetry_csv_export(tmp_path):
    tracker = TelemetryTracker()
    tracker.log(generation=1, best_fitness=100.0, mutation_rate=0.1)
    
    # tmp_path is a built-in pytest fixture providing a temporary directory
    file_path = tmp_path / "test_telemetry.csv"
    
    tracker.export_to_csv(str(file_path))
    
    # Assert file was created
    assert file_path.exists()
    
    # Read back and verify content
    content = file_path.read_text()
    assert "generation,best_fitness,mutation_rate" in content
    assert "1,100.0,0.1" in content