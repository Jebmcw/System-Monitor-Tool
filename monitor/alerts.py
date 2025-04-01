import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from monitor import cpu, memory, disk, network

def check_bottlenecks(console: Console):
    alerts = []
    warning_threshold = 80
    critical_threshold = 90
    rate_threshold = 12.5e6  # 12.5 MB/s = 100 Mbps

    # CPU
    cpu_data = cpu.get_cpu_data()
    cpu_usage = cpu_data["total_usage"]
    if cpu_usage >= critical_threshold:
        alerts.append(f"🔥 [bold red]High CPU usage:[/bold red] {cpu_usage:.1f}%")
    elif cpu_usage >= warning_threshold:
        alerts.append(f"⚠️ [yellow]Elevated CPU usage:[/yellow] {cpu_usage:.1f}%")

    # Memory
    mem_data = memory.get_memory_data()
    mem_usage = mem_data["percent"]
    used_gb = mem_data["used"] / 1e9
    total_gb = mem_data["total"] / 1e9
    if mem_usage >= critical_threshold:
        alerts.append(f"🧠 [bold red]High Memory usage:[/bold red] {used_gb:.1f} GB / {total_gb:.1f} GB ({mem_usage:.1f}%)")
    elif mem_usage >= warning_threshold:
        alerts.append(f"⚠️ [yellow]Elevated Memory usage:[/yellow] {used_gb:.1f} GB / {total_gb:.1f} GB ({mem_usage:.1f}%)")

    # Disk
    disk_data = disk.get_disk_data()
    for part in disk_data["partitions"]:
        part_usage = part["percent"]
        if part_usage >= critical_threshold:
            alerts.append(f"💽 [bold red]Disk nearly full:[/bold red] {part['mountpoint']} @ {part_usage:.1f}%")
        elif part_usage >= warning_threshold:
            alerts.append(f"💽 [yellow]Disk warning:[/yellow] {part['mountpoint']} @ {part_usage:.1f}%")

    disk_usages = {p["mountpoint"]: p["percent"] for p in disk_data["partitions"]}

    

    # Output
    if alerts:
        console.print(Panel.fit("\n".join(alerts), title="🚨 Bottleneck Detected", style="bold red"))
    else:
        console.print(Panel.fit("✅ All systems within normal limits", title="System Status", style="green"))

    # Summary chart
    print_usage_summary(console, cpu_usage, mem_usage, disk_usages)

def print_usage_summary(console, cpu_usage, mem_usage, disk_usages):
    table = Table(title="Component Usage Summary")
    table.add_column("Component", style="cyan")
    table.add_column("Usage", justify="right", style="magenta")

    table.add_row("CPU", f"{cpu_usage:.1f}%")
    table.add_row("Memory", f"{mem_usage:.1f}%")
    for part, usage in disk_usages.items():
        table.add_row(f"Disk {part}", f"{usage:.1f}%")

    console.print(table)


