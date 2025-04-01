import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from monitor import memory

def save_memory_table(memory_data):
    table_data = [["Type", "Used", "Total", "Usage (%)"]]

    # RAM row
    table_data.append([
        "RAM",
        f"{memory_data['used'] / 1e9:.2f} GB",
        f"{memory_data['total'] / 1e9:.2f} GB",
        f"{memory_data['percent']:.1f}%"
    ])

    # Swap row
    table_data.append([
        "Swap",
        f"{memory_data['swap_used'] / 1e9:.2f} GB",
        f"{memory_data['swap_total'] / 1e9:.2f} GB",
        f"{memory_data['swap_percent']:.1f}%"
    ])

    # Setup figure
    fig, ax = plt.subplots(figsize=(6, 0.5 + 0.4 * len(table_data)))
    ax.axis('off')

    # Draw table
    table = ax.table(
        cellText=table_data,
        colLabels=None,
        loc='center',
        cellLoc='center'
    )

    table.scale(1, 1.5)
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Save to file
    output_dir = 'first_demo_charts'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'memory_usage_table.png'), bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    memory_data = memory.get_memory_data()
    save_memory_table(memory_data)