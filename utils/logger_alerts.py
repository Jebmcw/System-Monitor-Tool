import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from monitor import cpu, memory, disk, network

def save_alert_summary_chart(output_path="first_demo_charts/alert_summary_table.png"):
    # Collect data
    cpu_data = cpu.get_cpu_data()
    mem_data = memory.get_memory_data()
    disk_data = disk.get_disk_data()
    net_data = network.get_network_rate()

    cpu_usage = cpu_data["total_usage"]
    mem_usage = mem_data["percent"]
    disk_usages = {p["mountpoint"]: p["percent"] for p in disk_data["partitions"]}
    net_sent = net_data["sent_per_sec"]
    net_recv = net_data["recv_per_sec"]

    # Build table data
    table_data = [["Component", "Usage"]]
    table_data.append(["CPU", f"{cpu_usage:.1f}%"])
    table_data.append(["Memory", f"{mem_usage:.1f}%"])

    for part, usage in disk_usages.items():
        table_data.append([f"Disk {part}", f"{usage:.1f}%"])

    table_data.append(["Net Sent", f"{net_sent / 1e6:.2f} MB/s"])
    table_data.append(["Net Recv", f"{net_recv / 1e6:.2f} MB/s" if net_recv >= 1e6 else f"{net_recv / 1e3:.2f} KB/s"])

    # Setup plot
    fig, ax = plt.subplots(figsize=(6, 0.5 + 0.4 * len(table_data)))
    ax.axis('off')

    table = ax.table(
        cellText=table_data,
        colLabels=None,
        loc='center',
        cellLoc='center'
    )
    table.scale(1, 1.5)
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Save the image
    os.makedirs("first_demo_charts", exist_ok=True)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    save_alert_summary_chart()
