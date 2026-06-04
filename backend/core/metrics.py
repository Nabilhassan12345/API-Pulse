import psutil
from typing import Dict, Any

def get_system_metrics() -> Dict[str, Any]:
    return {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": psutil.virtual_memory().percent,
        "memory_used_mb": round(psutil.virtual_memory().used / (1024 * 1024), 2),
        "memory_total_mb": round(psutil.virtual_memory().total / (1024 * 1024), 2)
    }
