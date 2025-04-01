import psutil
from rich.console import Console

def get_cpu_data():
    # Prime psutil to avoid 0.0% readings on first call
    psutil.cpu_percent(interval=None)

    usage_per_core = psutil.cpu_percent(interval=None, percpu=True)
    total_usage = sum(usage_per_core) / len(usage_per_core)  # average
    freq = psutil.cpu_freq()
    core_count = psutil.cpu_count(logical=True)

    return {
        "usage_per_core": usage_per_core,
        "total_usage": total_usage,
        "core_count": core_count,
        "freq": {
            "current": freq.current if freq else None,
            "min": freq.min if freq else None,
            "max": freq.max if freq else None
        }
    }

def print_cpu_usage(console: Console):
    _ = get_cpu_data()
    console.print("[green]CPU data successfully grabbed.[/green]")
