import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from monitor import network

def save_network_table(network_data):
    interfaces = network_data["interfaces"]  # ← this is the correct list

    # Add total and rate summary under the table
    summary = network_data["summary"]
    rate = network.get_network_rate(interval=1.0)
    
    total_sent = summary["total_sent"] / 1e6
    total_recv = summary["total_recv"] / 1e6
    sent_rate = rate["sent_per_sec"] / 1e6
    recv_rate_val = rate["recv_per_sec"]
    recv_rate = f"{recv_rate_val / 1e6:.2f} MB/s" if recv_rate_val >= 1e6 else f"{recv_rate_val / 1e3:.2f} KB/s"

    summary_text = (
        f"Total Sent: {total_sent:.2f} MB\n"
        f"Total Received: {total_recv:.2f} MB\n"
        f"Send Rate: {sent_rate:.2f} MB/s\n"
        f"Receive Rate: {recv_rate}"
        )

    table_data = [["Interface", "Sent (MB)", "Recv (MB)", "Packets Sent", "Packets Recv"]]

    for iface in interfaces:
        table_data.append([
            iface["name"],
            f"{iface['bytes_sent'] / 1e6:.2f}",
            f"{iface['bytes_recv'] / 1e6:.2f}",
            f"{iface['packets_sent']}",
            f"{iface['packets_recv']}"
        ])

    # Setup figure
    fig, ax = plt.subplots(figsize=(6, 0.5 + 0.4 * len(table_data) + 1.0))
    ax.axis('off')

    # Draw table
    table = ax.table(
        cellText=table_data,
        colLabels=None,
        loc='center',
        cellLoc='center'
    )

    table.scale(2.5, 5.5)
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)

    # Add to plot (position: below table)
    plt.text(-.5, -.5, summary_text, ha='center', va='top', transform=ax.transAxes, fontsize=10)

    # Save to file
    output_dir = 'first_demo_charts'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'network_usage_table.png'), bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    network_data = network.get_network_data()
    save_network_table(network_data)