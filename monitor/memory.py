import psutil
from rich.table import Table
from rich.console import Console

def get_memory_data():
    
    # Returns total, used, free, and % for RAM and swap.
    virtual = psutil.virtual_memory()
    swap = psutil.swap_memory()

    return{
        "total": virtual.total,
        "used": virtual.used,
        "free": virtual.available,
        "percent": virtual.percent,
        "swap_total": swap.total,
        "swap_used": swap.used,
        "swap_percent": swap.percent
    }

def print_memory_usage(console: Console):
    data = get_memory_data()
    table = Table(title="Memory Usage")

    table.add_column("Type", style="cyan")
    table.add_column("Used", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Usage (%)", justify="right", style="magenta")

    table.add_row(
        "RAM",
        f"{data['used'] / 1e9:.2f} GB",
        f"{data['total'] / 1e9:.2f} GB",
        f"{data['percent']:.1f}%"
    )

    table.add_row(
        "Swap",
        f"{data['swap_used'] / 1e9:.2f} GB",
        f"{data['swap_total'] / 1e9:.2f} GB",
        f"{data['swap_percent']:.1f}%"
    )

    console.print(table)