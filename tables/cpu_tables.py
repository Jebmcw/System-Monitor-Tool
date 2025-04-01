import threading
import time
import psutil
import tkinter as tk
from tkinter import ttk

class LiveCPUTracker:
    def __init__(self, callback):
        self.callback = callback  # Function to update GUI
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self._run, daemon=True).start()

    def stop(self):
        self.running = False

    def _run(self):
        psutil.cpu_percent(interval=None)  # Prime counters
        while self.running:
            usage_per_core = psutil.cpu_percent(interval=1.0, percpu=True)
            total_usage = sum(usage_per_core) / len(usage_per_core)
            freq = psutil.cpu_freq()
            data = {
                "usage_per_core": usage_per_core,
                "total_usage": total_usage,
                "freq": freq.current if freq else None,
            }
            self.callback(data)  # Let GUI update safely

class LiveCPUTable(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=("Core", "Usage"), show="headings", height=10)
        self.tree.heading("Core", text="Core")
        self.tree.heading("Usage", text="Usage (%)")
        self.tree.pack(expand=True, fill="both")
        self.cpu_tracker = LiveCPUTracker(self.schedule_update)
        self.cpu_tracker.start()

    def schedule_update(self, data):
        self.after(0, lambda: self.update_table(data))  # Schedule safely on main thread

    def update_table(self, data):
        self.tree.delete(*self.tree.get_children())
        for i, usage in enumerate(data["usage_per_core"]):
            self.tree.insert("", "end", values=(f"Core {i}", f"{usage:.1f}%"))
        self.tree.insert("", "end", values=("Total", f"{data['total_usage']:.1f}%"))
        self.tree.insert("", "end", values=("Freq", f"{data['freq']:.1f} MHz"))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x400")
    root.title("CPU Monitor")

    cpu_widget = LiveCPUTable(root)
    cpu_widget.pack(expand=True, fill="both")

    root.mainloop()
