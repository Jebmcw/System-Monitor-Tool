import psutil
from rich.table import Table
from rich.console import Console

def get_disk_data():

    # Collects usage stats for all mounted disk partitions and overall I/O counters.
    # Returns a list of partition data and global I/O stats.

    partitions = psutil.disk_partitions()
    usage_data = []

    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            usage_data.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "used": usage.used,
                "total": usage.total,
                "percent": usage.percent
            })
        except PermissionError:
            continue # Ignore drives that can't be accessed

    io = psutil.disk_io_counters()

    return {
        "partitions": usage_data,
        "io": {
            "read_mb": io.read_bytes / 1e6,
            "write_mb": io.write_bytes / 1e6
        }
    }

def print_disk_usage(console: Console):
    data = get_disk_data()

    table = Table(title="Disk Usage per Partition")
    table.add_column("Device", style="cyan")
    table.add_column("Mount", style="white")
    table.add_column("Type", justify="right")
    table.add_column("Used", justify="right")
    table.add_column("Total", justify="right")
    table.add_column("Usage (%)", justify="right", style="magenta")

    for part in data["partitions"]:
        table.add_row(
            part["device"],
            part["mountpoint"],
            part["fstype"],
            f"{part['used'] / 1e9:.2f} GB",
            f"{part['total'] / 1e9:.2f} GB",
            f"{part['percent']:.1f}%"
        )

    console.print(table)

    # I/O summary (read/write totals)
    io = data["io"]
    console.print(f"[bold yellow]Total Read:[/bold yellow] {io['read_mb']:.2f} MB")
    console.print(f"[bold yellow]Total Write:[/bold yellow] {io['write_mb']:.2f} MB")