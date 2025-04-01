import sys
import os
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from monitor import cpu

def save_cpu_table(cpu_data):
    usage_per_core = cpu_data["usage_per_core"]

    # Build table data: headers + core usage rows
    table_data = [["Core", "Usage (%)"]]
    for i, usage in enumerate(usage_per_core):
        table_data.append([f"Core {i}", f"{usage:.1f}%"])

    table_data.append(["Total", f"{cpu_data['total_usage']:.1f}%"])
    table_data.append(["Freq (MHz)", f"{cpu_data['freq']['current']:.1f}"])

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(5, 0.5 + 0.4 * len(table_data)))  # Dynamic height
    ax.axis('off')  # No axis lines

    # Draw the table
    table = ax.table(
        cellText=table_data,
        colLabels=None,
        loc='center',
        cellLoc='center'
    )

    # Color the "Usage (%)" column cells based on thresholds
    for row_idx in range(1, len(table_data) - 2):  # Skip header + last 2 rows (Total, Freq)
        usage_str = table_data[row_idx][1].replace('%', '')
        usage_val = float(usage_str)

        cell = table[(row_idx, 1)]  # (row_index, column_index)

        if usage_val >= 10:
            cell.get_text().set_color('red')
        elif usage_val >= 5:
            cell.get_text().set_color('orange')
        else:
            cell.get_text().set_color('green')
    
    table.scale(1, 1.5)
    table.auto_set_font_size(False)
    table.set_fontsize(10)

    # Save to file
    output_dir = 'first_demo_charts'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'cpu_usage_table.png'), bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    cpu_data = cpu.get_cpu_data()
    save_cpu_table(cpu_data)

