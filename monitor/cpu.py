import psutil
from rich.table import Table
from rich.console import Console

def get_cpu_data():

    # Get usage for each logical core over 1 second
    usage_per_core = psutil.cpu_percent(interval=1, percpu=True)

    # Get total CPU usage over 1 second
    total_usage = psutil.cpu_percent(interval=1)

    # Get current, min, and max CPU frequency
    freq = psutil.cpu_freq()

    # Get total number of logical CPU cores
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
    # Fetch the CPU data dictionary
    data = get_cpu_data()

    # Create a rich table to display CPU usage
    table = Table(title="CPU Usage")

    # Add table columns for core number and usage %
    table.add_column("Core", justify="right", style="cyan", no_wrap=True)
    table.add_column("Usage (%)", justify="right", style="magenta")

    # Add rows for each core's usage
    for i, percent in enumerate(data["usage_per_core"]):
        table.add_row(f"Core {i}", f"{percent:.1f}%")

    # Add total CPU usage
    table.add_row("Total", f"{data['total_usage']:.1f}%")

    # Add current CPU frequency
    table.add_row("Freq", f"{data['freq']['current']} MHz")

    # Print the table to the console
    console.print(table)
