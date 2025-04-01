import psutil
from rich.table import Table
from rich.console import Console
import time

def get_network_data():
    """
    Returns per-interface and global network usage.
    Reports total bytes sent/received and packet counts.
    """
    io = psutil.net_io_counters(pernic=True)
    summary = psutil.net_io_counters()

    interfaces = []
    for iface, stats in io.items():
        interfaces.append({
            "name": iface,
            "bytes_sent": stats.bytes_sent,
            "bytes_recv": stats.bytes_recv,
            "packets_sent": stats.packets_sent,
            "packets_recv": stats.packets_recv
        })

    return {
        "interfaces": interfaces,
        "summary": {
            "total_sent": summary.bytes_sent,
            "total_recv": summary.bytes_recv,
            "total_packets_sent": summary.packets_sent,
            "total_packets_recv": summary.packets_recv
        }
    }

def get_network_rate(interval=1.0):
    """
    Measures network send/recv rate (in bytes/sec) over a given interval.
    Returns rate in bytes/sec.
    """
    t0 = psutil.net_io_counters()
    time.sleep(interval)
    t1 = psutil.net_io_counters()

    sent_rate = (t1.bytes_sent - t0.bytes_sent) / interval
    recv_rate = (t1.bytes_recv - t0.bytes_recv) / interval

    return {
        "sent_per_sec": sent_rate,
        "recv_per_sec": recv_rate
    }

def print_network_stats(console: Console):
    # Pull interface stats
    data = get_network_data()

    # Print interface-level table
    table = Table(title="Network Interfaces")
    table.add_column("Interface", style="cyan")
    table.add_column("Sent (MB)", justify="right")
    table.add_column("Recv (MB)", justify="right")
    table.add_column("Packets Sent", justify="right")
    table.add_column("Packets Recv", justify="right")

    for iface in data["interfaces"]:
        table.add_row(
            iface["name"],
            f"{iface['bytes_sent'] / 1e6:.2f}",
            f"{iface['bytes_recv'] / 1e6:.2f}",
            f"{iface['packets_sent']}",
            f"{iface['packets_recv']}"
        )

    console.print(table)

    # Print global totals
    summary = data["summary"]
    console.print(f"[bold yellow]Total Sent:[/bold yellow] {summary['total_sent'] / 1e6:.2f} MB")
    console.print(f"[bold yellow]Total Received:[/bold yellow] {summary['total_recv'] / 1e6:.2f} MB")

    # Print live rate (after 1s interval)
    rate = get_network_rate(interval=1.0)
    console.print(f"[cyan]Send Rate:[/cyan] {rate['sent_per_sec'] / 1e6:.2f} MB/s")
    
    if rate['recv_per_sec'] >= 1e6:
        console.print(f"[cyan]Receive Rate:[/cyan] {rate['recv_per_sec'] / 1e6:.2f} MB/s")
    else:
        console.print(f"[cyan]Receive Rate:[/cyan] {rate['recv_per_sec'] / 1e3:.2f} KB/s")


