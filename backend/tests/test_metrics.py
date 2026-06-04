from core.metrics import get_system_metrics

def test_metrics_collection():
    metrics = get_system_metrics()
    assert "cpu_percent" in metrics
    assert "memory_percent" in metrics
    assert "memory_used_mb" in metrics
    assert "memory_total_mb" in metrics
    
    assert isinstance(metrics["cpu_percent"], (int, float))
    assert isinstance(metrics["memory_percent"], (int, float))
    assert metrics["memory_total_mb"] > 0
