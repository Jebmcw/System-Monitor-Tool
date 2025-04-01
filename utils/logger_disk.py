import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from monitor import disk

def save_disk_table(disk_data):
    partitions = disk_data["partitions"]

    # Prepare table data
    table_data = [["Mount", "Used (GB)", "Total (GB)", "Usage (%)"]]
    for part in partitions:
        table_data.append([
            part["mountpoint"],
            f"{part['used'] / 1e9:.2f}",
            f"{part['total'] / 1e9:.2f}",
            f"{part['percent']:.1f}%"
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

    # Optional: Color Usage % column
    for row_idx in range(1, len(table_data)):
        percent_str = table_data[row_idx][3].replace('%', '')
        percent_val = float(percent_str)
        cell = table[(row_idx, 3)]

        if percent_val >= 90:
            cell.get_text().set_color('red')
        elif percent_val >= 80:
            cell.get_text().set_color('orange')
        else:
            cell.get_text().set_color('black')

    # Save to file
    output_dir = 'first_demo_charts'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'disk_usage_table.png'), bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    disk_data = disk.get_disk_data()
    save_disk_table(disk_data)
